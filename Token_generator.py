from secrets import token_urlsafe

class TokenGenerator():
    def generate_token(self, length: int=16) -> str:
        return token_urlsafe(length) 

if __name__ == "__main__":
    token_generator = TokenGenerator()
    print(token_generator.generate_token())