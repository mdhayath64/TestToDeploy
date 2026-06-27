# _DeployToTest
# Simple Express.js Project

## How to Run

1. Install dependencies:
	```
	npm install
	```
2. Configure `.env`:
	```
	PORT=8000
	MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
	MONGODB_DB_NAME=sample_db
	MONGODB_COLLECTION_NAME=items
	```
3. Start the server:
	```
	npm start
	```
4. To run on a custom port, change `PORT` in `.env` (for example `3000`) and restart the app.

Alternative without `.env`:
	```
	# PowerShell
	$env:PORT=3000; npm start
	```
5. Open your browser and go to [http://localhost:8000](http://localhost:8000)

You should see:

	 Hello, world!

## APIs

1. Get items list:
	- `GET /api/items`
	- Optional query: `limit` (default `20`, max `100`)

2. Get single item by id:
	- `GET /api/items/:id`
	- Example: `/api/items/6652a8b5f0f22eb1b8d5f70c`

3. Add item:
	- `POST /api/items`
	- Body: JSON object (non-empty)
	- Example body:
	```
	{
	  "name": "Sample Item",
	  "price": 25
	}
	```
	Powershell example:
	```
	Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/items" -ContentType "application/json" -Body '{"name":"Sample Item","price":25}'
 	```
