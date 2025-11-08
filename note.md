variables, description
rssd9001, "bank id"
wrdsreportdate, "date"
rssd9017, "bank name"
rssd9220, "zip code"
rssd9200, "state"
rssd9130, "city"
rssdfininstfilingtype, "filing type"

For EACH uploaded PDF, output a JSON block with:
- citekey: "AuthorYear"
- full_citation: APA style
- research_question: one sentence
- setting/data: country, years, sample size, datasets
- method: model/design; identification strategy if causal
- key_mechanisms: bullets
- main_findings: 3–6 bullets with magnitudes + units (each with page number)
- limits/caveats: bullets (with page if stated)
- how_it_relates_to_my_project: 2–4 bullets; refer to the research proposal in file folder
- notable_quotes: [{"page": X, "quote": "verbatim ≤40 words"}]
Rules: Use ONLY the uploaded PDFs. Every numeric claim gets a page citation. No outside sources. If info is missing, say “insufficient in paper.”