import typer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from tqdm import tqdm
from jsonsempai import magic
import ChatbotCorpus


def check_result(result, match):
    matches = result.get("data", {}).get("matchPhrase", [])
    if not matches:
        return False

    return (
        " ".join([m["search_phrase_word"].lower() for m in matches["word_matches"]])
        == match.lower()
    )


def main(url: str, admin_secret: str):
    transport = AIOHTTPTransport(
        url=url, headers={"x-hasura-admin-secret": admin_secret}
    )
    client = Client(transport=transport, execute_timeout=120)

    success, count, errors = 0, 0, 0
    for sentence in tqdm(ChatbotCorpus.sentences):
        search_phrases = ", ".join([f'"{s}"' for s in sentence.templates])
        for input_ in sentence.inputs:
            query_str = f"""
            query {{
                matchPhrase(phrase:"{input_}", search_phrases:[{search_phrases}], debug:true) {{
                    word_matches {{
                        search_phrase_word
                    }}
                }}
            }}
            """
            query = gql(query_str)
            try:
                result = client.execute(query)
                if result["matchPhrase"]:
                    print("-->", result, sentence.match)
            except Exception as e:
                errors += 1
                print("++", e)
                continue
            if check_result(result, sentence.match):
                success += 1
                break
        count += 1
    print(f"{success} successful out of {count}, query errors: {errors}")


if __name__ == "__main__":
    typer.run(main)
