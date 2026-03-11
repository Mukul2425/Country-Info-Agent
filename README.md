# Country Information AI Agent

An AI-powered country information assistant that:
- Extracts intent from natural language questions
- Fetches live country data from the REST Countries API
- Synthesizes a concise final answer

## Architecture

```text
User Question
	|
	v
Intent Identification (Gemini)
	|
	v
LangGraph Router
	|
	+-- Invalid Input -> Error Response
	|
	v
REST Countries API Tool
	|
	v
Answer Synthesis
	|
	v
Final Response
```

## Agent Flow

### Example Question
`What is the capital and population of Brazil?`

### Step 1 - Intent Extraction

```text
country = Brazil
fields = capital, population
```

### Step 2 - Tool Invocation

Call:

```text
https://restcountries.com/v3.1/name/brazil
```

### Step 3 - Answer Synthesis

```text
Capital: Brasilia
Population: 213421037
```

## Example API Request

### Endpoint
`POST /ask`

### Request

```json
{
  "question": "What currency does Japan use?"
}
```

### Response

```json
{
  "answer": "Currency: JPY"
}
```
