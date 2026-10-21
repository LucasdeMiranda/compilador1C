from enum import IntEnum

class TOKEN(IntEnum):
    # Palavras-chave
    INT = 1
    FLOAT = 2
    STRING = 3
    VOID = 4
    BREAK = 5
    CONTINUE = 6
    LOOP = 7
    WHILE = 8
    FOR = 9
    IN = 10
    IF = 11
    ELIF = 12
    ELSE = 13
    READ = 14
    WRITE = 15
    OR = 16
    AND = 17
    NOT = 18
    DIV = 19
    MOD = 20
    RETURN = 21

    # Identificadores e valores
    IDENT = 22
    INTNUM = 23
    FLOATNUM = 24
    STRINGCONST = 25

    # Operadores
    ATRIB = 26       # =
    OPREL = 27       # <, >, <=, >=, ==, !=
    MAIS = 28        # +
    MENOS = 29       # -
    MULT = 30        # *
    DIVIDE = 31      # /
    INCREM = 32      # ++
    DECREM = 33      # --
    ENDERECO = 34    # &

    # Delimitadores
    ABREPAR = 35     # (
    FECHAPAR = 36   # )
    ABRECHAVE = 37  # {
    FECHACHAVE = 38 # }
    ABRECOL = 39    # [
    FECHACOL = 40   # ]
    VIRGULA = 41    # ,
    PONTOVIRG = 42  # ;

    EOF = 43
    ERRO = 44

    @classmethod
    def msg(cls, token):
        nomes = {
            1: 'int',
            2: 'float',
            3: 'string',
            4: 'void',
            5: 'break',
            6: 'continue',
            7: 'loop',
            8: 'while',
            9: 'for',
            10: 'in',
            11: 'if',
            12: 'elif',
            13: 'else',
            14: 'read',
            15: 'write',
            16: 'OR',
            17: 'AND',
            18: 'NOT',
            19: 'div',
            20: 'mod',
            21: 'return',
            22: 'ident',
            23: 'intNumber',
            24: 'floatNumber',
            25: 'string',
            26: '=',
            27: 'opRel',
            28: '+',
            29: '-',
            30: '*',
            31: '/',
            32: '++',
            33: '--',
            34: '&',
            35: '(',
            36: ')',
            37: '{',
            38: '}',
            39: '[',
            40: ']',
            41: ',',
            42: ';',
            43: '<eof>',
            44: 'erro'
        }

        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'int': TOKEN.INT,
            'float': TOKEN.FLOAT,
            'string': TOKEN.STRING,
            'void': TOKEN.VOID,
            'break': TOKEN.BREAK,
            'continue': TOKEN.CONTINUE,
            'loop': TOKEN.LOOP,
            'while': TOKEN.WHILE,
            'for': TOKEN.FOR,
            'in': TOKEN.IN,
            'if': TOKEN.IF,
            'elif': TOKEN.ELIF,
            'else': TOKEN.ELSE,
            'read': TOKEN.READ,
            'write': TOKEN.WRITE,
            'OR': TOKEN.OR,
            'AND': TOKEN.AND,
            'NOT': TOKEN.NOT,
            'div': TOKEN.DIV,
            'mod': TOKEN.MOD,
            'return': TOKEN.RETURN,
        }

        return reservadas.get(lexema, TOKEN.IDENT)


    # Tabela de operações seguindo o padrão da linguagem C
    @classmethod
    def tabelaOperacoes(cls):
        return {

            # ------------------ Aritméticas ------------------

            ((TOKEN.INT, False), TOKEN.MAIS,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.MENOS,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.MULT,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.DIVIDE,
             (TOKEN.INT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.INT, False), TOKEN.DIV,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.MOD,
             (TOKEN.INT, False)) : (TOKEN.INT, False),


            ((TOKEN.FLOAT, False), TOKEN.MAIS,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.MENOS,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.MULT,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.DIVIDE,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),


            # INT + FLOAT
            ((TOKEN.INT, False), TOKEN.MAIS,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.MAIS,
             (TOKEN.INT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.INT, False), TOKEN.MENOS,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.MENOS,
             (TOKEN.INT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.INT, False), TOKEN.MULT,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.MULT,
             (TOKEN.INT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.INT, False), TOKEN.DIVIDE,
             (TOKEN.FLOAT, False)) : (TOKEN.FLOAT, False),

            ((TOKEN.FLOAT, False), TOKEN.DIVIDE,
             (TOKEN.INT, False)) : (TOKEN.FLOAT, False),


            # ------------------ Relacionais ------------------

            ((TOKEN.INT, False), TOKEN.OPREL,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.FLOAT, False), TOKEN.OPREL,
             (TOKEN.FLOAT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.OPREL,
             (TOKEN.FLOAT, False)) : (TOKEN.INT, False),

            ((TOKEN.FLOAT, False), TOKEN.OPREL,
             (TOKEN.INT, False)) : (TOKEN.INT, False),


            # ------------------ Lógicos ------------------

            ((TOKEN.INT, False), TOKEN.AND,
             (TOKEN.INT, False)) : (TOKEN.INT, False),

            ((TOKEN.INT, False), TOKEN.OR,
             (TOKEN.INT, False)) : (TOKEN.INT, False),


            # NOT unário
            (TOKEN.NOT, (TOKEN.INT, False)) :
                (TOKEN.INT, False),


            # ------------------ Unários ------------------

            (TOKEN.MAIS, (TOKEN.INT, False)) :
                (TOKEN.INT, False),

            (TOKEN.MENOS, (TOKEN.INT, False)) :
                (TOKEN.INT, False),

            (TOKEN.MAIS, (TOKEN.FLOAT, False)) :
                (TOKEN.FLOAT, False),

            (TOKEN.MENOS, (TOKEN.FLOAT, False)) :
                (TOKEN.FLOAT, False),
        }


