FAQS = [
	{
		"q": "How do I open an account?",
		"a": "To open an account, bring a valid photo ID and proof of address to any branch or apply online. You will choose the account type and may need a small initial deposit.",
		"keywords": ["open", "account", "apply", "how to"]
	},
	{
		"q": "When does the bank close?",
		"a": "Most branches operate 9:00 AM to 5:00 PM Monday to Friday; some branches have extended hours. Check your local branch for exact times.",
		"keywords": ["close", "closing", "hours", "open"]
	},
	{
		"q": "How can I contact customer support?",
		"a": "Call our 24/7 support at 1-800-EXAMPLE or email support@examplebank.com. For branch-specific queries, visit the branch page on our website.",
		"keywords": ["contact", "support", "help", "customer"]
	},
	{
		"q": "What are the fees for monthly maintenance?",
		"a": "Our standard checking account has a $5 monthly maintenance fee which can be waived if you meet minimum balance or direct deposit requirements. See fee schedule on our website.",
		"keywords": ["fee", "fees", "maintenance", "monthly"]
	},
	{
		"q": "What is the interest rate on savings?",
		"a": "Savings rates vary by product and location. Current rates are posted on our website and updated regularly. Contact support for the latest rate for your account.",
		"keywords": ["interest", "rate", "savings", "APR"]
	},
	{
		"q": "How do I report a lost or stolen card?",
		"a": "Report a lost or stolen card immediately via our 24/7 support line or through online banking to block the card and request a replacement.",
		"keywords": ["lost", "stolen", "card", "report"]
	},
	{
		"q": "What documents are required to open a business account?",
		"a": "Business accounts typically require business registration documents, taxpayer ID, and identification for all signers. Requirements vary by business type.",
		"keywords": ["business", "documents", "required", "open"]
	},
	{
		"q": "What are ATM withdrawal limits?",
		"a": "Daily ATM withdrawal limits depend on account type; a typical limit is $500 per day. For larger withdrawals, contact your branch.",
		"keywords": ["atm", "withdrawal", "limit", "limits"]
	}
]

RAG_DOCS = [
	{
		"title": "Bank Overview",
		"text": (
			"ExampleBank is a regional financial institution focused on retail and small-business banking. "
			"We offer checking, savings, loans, and digital banking services with an emphasis on community service and security."
		),
		"keywords": ["overview", "about", "who we are", "examplebank"]
	},
	{
		"title": "Security & Privacy",
		"text": (
			"We use multi-factor authentication, encryption, and continuous monitoring to protect customer data. "
			"Never share your full password or PIN; contact support immediately if you suspect compromise."
		),
		"keywords": ["security", "privacy", "safe", "protect"]
	},
	{
		"title": "Services",
		"text": (
			"Services include personal and business checking/savings, mortgages, auto loans, online banking, mobile deposits, and merchant services. "
			"Visit a branch or our website for product comparisons."
		),
		"keywords": ["services", "products", "mortgage", "loans", "online banking"]
	}
]