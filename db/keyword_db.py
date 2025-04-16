# keyword_db.py
async def load_keyword_responses(pool):
    async with pool.acquire() as conn:
        records = await conn.fetch("SELECT * FROM keyword_responses")
        responses = {}
        for record in records:
            keyword = record['keyword']
            responses[keyword] = {
                "user_id": record['user_id'],
                "random": record['random'],
                "type": record['response_type'],
                "content": record['content'],
                "emoji": record['emoji'],
                "gif_url": record['gif_url'],
                "responses": []  # Load from variant table if random=True
            }
            if record['random']:
                variants = await conn.fetch("SELECT response FROM keyword_response_variants WHERE keyword=$1", keyword)
                responses[keyword]["responses"] = [v["response"] for v in variants]
        return responses

async def update_keyword_response(pool, keyword, data):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO keyword_responses (keyword, user_id, response_type, content, emoji, gif_url, random)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (keyword) DO UPDATE
            SET user_id=$2, response_type=$3, content=$4, emoji=$5, gif_url=$6, random=$7
        """, keyword, data["user_id"], data["type"], data["content"], data["emoji"], data["gif_url"], data["random"])

        if data["random"]:
            await conn.execute("DELETE FROM keyword_response_variants WHERE keyword=$1", keyword)
            for r in data["responses"]:
                await conn.execute("INSERT INTO keyword_response_variants (keyword, response) VALUES ($1, $2)", keyword, r)

async def remove_keyword(pool, keyword):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM keyword_responses WHERE keyword = $1", keyword)
