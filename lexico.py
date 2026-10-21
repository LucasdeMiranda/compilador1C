from token import TOKEN


class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte
        self.fonte = self.arqFonte.read()
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.linha = 1
        self.coluna = 0
        self.tokenLido = None  # (token, lexema, linha, coluna)

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    def getchar(self):
        if self.fimDoArquivo():
            return '\0'

        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1

        if car == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1

        return car

    def ungetchar(self):
        if self.indiceFonte > 0:
            self.indiceFonte -= 1
            self.coluna -= 1

    def descartacomentarios(self):
        simbolo = self.getchar()

        while simbolo not in ['\n', '\0']:
            simbolo = self.getchar()

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente

        msg = TOKEN.msg(token)

        VERDE = "\033[92m"
        RESET = "\033[0m"

        print(
            f'(tk={VERDE}{msg}{RESET} '
            f'lex={VERDE}"{lexema}"{RESET} '
            f'lin={linha} col={coluna})'
        )

    def getToken(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''

        lin = self.linha
        col = self.coluna

        while True:

            # ignora espaços e quebras
            while simbolo in [' ', '\t', '\r', '\n']:
                simbolo = self.getchar()
                lin = self.linha
                col = self.coluna

            # ==============================
            # ESTADO 1 - INÍCIO
            # ==============================
            if estado == 1:

                # Identificador ou palavra reservada
                # [a-zA-Z][a-zA-Z0-9_]*
                if simbolo.isalpha():
                    estado = 2

                # Número
                elif simbolo.isdigit():
                    estado = 3

                # String
                elif simbolo == '"':
                    estado = 4

                # Parênteses
                elif simbolo == '(':
                    return (TOKEN.ABREPAR, "(", lin, col)

                elif simbolo == ')':
                    return (TOKEN.FECHAPAR, ")", lin, col)

                # Chaves
                elif simbolo == '{':
                    return (TOKEN.ABRECHAVE, "{", lin, col)

                elif simbolo == '}':
                    return (TOKEN.FECHACHAVE, "}", lin, col)

                # Colchetes
                elif simbolo == '[':
                    return (TOKEN.ABRECOL, "[", lin, col)

                elif simbolo == ']':
                    return (TOKEN.FECHACOL, "]", lin, col)

                # Vírgula
                elif simbolo == ',':
                    return (TOKEN.VIRGULA, ",", lin, col)

                # Ponto e vírgula
                elif simbolo == ';':
                    return (TOKEN.PONTOVIRG, ";", lin, col)

                # Mais
                elif simbolo == '+':
                    estado = 10

                # Menos
                elif simbolo == '-':
                    estado = 11

                # Multiplicação
                elif simbolo == '*':
                    return (TOKEN.MULT, "*", lin, col)

                # Divisão ou comentário
                elif simbolo == '/':
                    estado = 8

                # Atribuição ou igualdade
                elif simbolo == '=':
                    estado = 5

                # Menor
                elif simbolo == '<':
                    estado = 6

                # Maior
                elif simbolo == '>':
                    estado = 7

                # &
                elif simbolo == '&':
                    return (TOKEN.ENDERECO, "&", lin, col)

                # Fim do arquivo
                elif simbolo == '\0':
                    return (TOKEN.EOF, "<eof>", lin, col)

                else:
                    lexema += simbolo
                    return (TOKEN.ERRO, lexema, lin, col)


            # ==============================
            # ESTADO 2 - IDENTIFICADOR
            # ==============================
            elif estado == 2:

                while simbolo.isalnum() or simbolo == "_":
                    lexema += simbolo
                    simbolo = self.getchar()

                self.ungetchar()

                token = TOKEN.reservada(lexema)

                return (token, lexema, lin, col)


            # ==============================
            # ESTADO 3 - NÚMEROS
            # ==============================
            elif estado == 3:

                while simbolo.isdigit():
                    lexema += simbolo
                    simbolo = self.getchar()

                # possível float
                if simbolo == '.':

                    lexema += simbolo
                    simbolo = self.getchar()

                    while simbolo.isdigit():
                        lexema += simbolo
                        simbolo = self.getchar()

                    # Exemplo: 12.3abc
                    if simbolo.isalpha() or simbolo == "_":

                        while simbolo.isalnum() or simbolo == "_":
                            lexema += simbolo
                            simbolo = self.getchar()

                        return (TOKEN.ERRO, lexema, lin, col)

                    self.ungetchar()

                    return (TOKEN.FLOATNUM, lexema, lin, col)

                # Exemplo: 123abc
                elif simbolo.isalpha() or simbolo == "_":

                    while simbolo.isalnum() or simbolo == "_":
                        lexema += simbolo
                        simbolo = self.getchar()

                    return (TOKEN.ERRO, lexema, lin, col)

                else:

                    self.ungetchar()

                    return (TOKEN.INTNUM, lexema, lin, col)


            # ==============================
            # ESTADO 4 - STRING
            # ==============================
            elif estado == 4:

                simbolo = self.getchar()

                while simbolo != '"' and simbolo != '\0':

                    # Permite caracteres escapados
                    if simbolo == '\\':

                        lexema += simbolo
                        simbolo = self.getchar()

                        if simbolo == '\0':
                            return (TOKEN.ERRO, lexema, lin, col)

                    lexema += simbolo
                    simbolo = self.getchar()

                if simbolo == '\0':
                    return (TOKEN.ERRO, lexema, lin, col)

                return (TOKEN.STRINGCONST, lexema, lin, col)


            # ==============================
            # ESTADO 5 - "=" OU "=="
            # ==============================
            elif estado == 5:

                simbolo = self.getchar()

                if simbolo == '=':
                    return (TOKEN.OPREL, "==", lin, col)

                else:
                    self.ungetchar()
                    return (TOKEN.ATRIB, "=", lin, col)


            # ==============================
            # ESTADO 6 - "<" OU "<="
            # ==============================
            elif estado == 6:

                simbolo = self.getchar()

                if simbolo == '=':
                    return (TOKEN.OPREL, "<=", lin, col)

                else:
                    self.ungetchar()
                    return (TOKEN.OPREL, "<", lin, col)


            # ==============================
            # ESTADO 7 - ">" OU ">="
            # ==============================
            elif estado == 7:

                simbolo = self.getchar()

                if simbolo == '=':
                    return (TOKEN.OPREL, ">=", lin, col)

                else:
                    self.ungetchar()
                    return (TOKEN.OPREL, ">", lin, col)


            # ==============================
            # ESTADO 8 - "/" OU "//" (comentário)
            # ==============================
            elif estado == 8:

                proximo = self.getchar()

                if proximo == "/":

                    # comentário
                    self.descartacomentarios()

                    return self.getToken()

                else:

                    self.ungetchar()

                    return (TOKEN.DIVIDE, "/", lin, col)


            # ==============================
            # ESTADO 10 - "+" OU "++"
            # ==============================
            elif estado == 10:

                proximo = self.getchar()

                if proximo == '+':
                    return (TOKEN.INCREM, "++", lin, col)

                else:
                    self.ungetchar()
                    return (TOKEN.MAIS, "+", lin, col)


            # ==============================
            # ESTADO 11 - "-" OU "--"
            # ==============================
            elif estado == 11:

                proximo = self.getchar()

                if proximo == '-':
                    return (TOKEN.DECREM, "--", lin, col)

                else:
                    self.ungetchar()
                    return (TOKEN.MENOS, "-", lin, col)


if __name__ == "__main__":

    caminho = r"/home/lucas/Área de trabalho/compilador1C/teste.txt"

    try:

        with open(caminho, 'r', encoding='utf-8') as arquivo:

            lexico = Lexico(arquivo)

            while True:

                token_corrente = lexico.getToken()

                lexico.imprimeToken(token_corrente)

                if token_corrente[0] == TOKEN.EOF:
                    break

    except FileNotFoundError:

        print(f"Arquivo não encontrado: {caminho}")

    except Exception as e:

        print(f"Ocorreu um erro: {e}")
 

