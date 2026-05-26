import torch
from transformers import AutoTokenizer, AutoModel
from data import FAQS, RAG_DOCS

class SimpleRAG:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print("Initializing local RAG Embedding Model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
        # Combine FAQs and general RAG documents
        self.documents = FAQS + RAG_DOCS
        self.texts = []
        for doc in self.documents:
            if "q" in doc and "a" in doc:
                text = f"Question: {doc['q']}\nAnswer: {doc['a']}"
            else:
                text = f"Title: {doc['title']}\nContent: {doc['text']}"
            self.texts.append(text)
        
        # Precompute embeddings
        self.doc_embeddings = self._embed(self.texts)
        print("RAG initialized successfully.")

    def _embed(self, texts):
        # Tokenize sentences
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        
        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        
        # Perform mean pooling
        token_embeddings = model_output[0]
        attention_mask = encoded_input['attention_mask']
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        embeddings = sum_embeddings / sum_mask
        
        # Normalize embeddings to unit length (for cosine similarity via simple dot product)
        return torch.nn.functional.normalize(embeddings, p=2, dim=1)

    def retrieve(self, query, k=2):
        """
        Retrieves the top-k matches for a query using cosine similarity.
        Returns a string of formatted context for the LLM system prompt.
        """
        if not self.documents:
            return ""
            
        q_emb = self._embed([query])
        
        # Dot product of normalized vectors equals Cosine Similarity
        scores = torch.matmul(self.doc_embeddings, q_emb.T).squeeze(-1)
        
        # Get top-k indices
        top_k = torch.topk(scores, k=min(k, len(self.documents)))
        indices = top_k.indices.tolist()
        
        results = []
        for idx in indices:
            results.append(self.texts[idx])
            
        return "\n\n".join(results)
