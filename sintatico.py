from lexico import TOKEN, Lexico
class Sintatico:

    def __init__(self, lexico: Lexico):
        self.lexico = lexico
        self.lexico.tokenLido = self.lexico.getToken()

    def consome(self, tokenesperado):
        (token, lexema, linha, coluna) = self.lexico.tokenLido
        if token == TOKEN.STRINGCONST:
            lexema = f'"{lexema}"'
        if token == tokenesperado:
            self.lexico.tokenLido = self.lexico.getToken()
        else:
            msgtokenlido = TOKEN.msg(token)
            msgtokenatual = TOKEN.msg(tokenesperado)
            msg = lexema if token == TOKEN.ERRO else msgtokenlido
            print(f"Erro Sintático na linha {linha}, coluna {coluna}:")
            print(f"Esperava-se {msgtokenatual}, mas veio {msg}")
            raise Exception("Erro Sintático")

    def inicio(self):
        self.Program()

    # ---------------------------
    # Prog -> Func RestoProg
    # RestoProg -> LAMBDA | Func RestoProg
    # ---------------------------
    def Program(self):
        while self.lexico.tokenLido[0] in (
            TOKEN.INT,
            TOKEN.FLOAT,
            TOKEN.STRING,
            TOKEN.VOID,
        ):
            self.Function()

    # ---------------------------
    # Func -> TipoFunc ident ( ListaArgs ) Corpo
    # ---------------------------
    def Function(self):
        self.TipoFunc()
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.ABREPAR)
        self.ListaArgs()
        self.consome(TOKEN.FECHAPAR)
        self.Corpo()

    # TipoFunc -> void | TipoPrim
    def TipoFunc(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.VOID:
            self.consome(TOKEN.VOID)
        else:
            self.TipoPrim()
 
    # TipoPrim -> int | float | string
    
    def TipoPrim(self):
        token = self.lexico.tokenLido[0]
        if token in (TOKEN.INT, TOKEN.FLOAT, TOKEN.STRING):
            self.consome(token)
        else:
            raise Exception(
                f"Erro Sintático na linha {self.lexico.linha}: Tipo esperado"
            )
 
    # ListaArgs -> LAMBDA | Arg RestoListaArgs
 
    def ListaArgs(self):
        token = self.lexico.tokenLido[0]
        if token in (TOKEN.INT, TOKEN.FLOAT, TOKEN.STRING):
            self.Arg()
            self.RestoListaArgs()

    # ---------------------------
    # RestoListaArgs -> , Arg RestoListaArgs | LAMBDA
    # ---------------------------
    def RestoListaArgs(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.Arg()
            self.RestoListaArgs()

    # ---------------------------
    # Arg -> TipoPrim OpcRef ident OpcColchete
    # ---------------------------
    def Arg(self):
        self.TipoPrim()
        self.OpcRef()
        self.consome(TOKEN.IDENT)
        self.OpcColchete()

    # ---------------------------
    # OpcRef -> LAMBDA | &
    # ---------------------------
    def OpcRef(self):
        if self.lexico.tokenLido[0] == TOKEN.ENDERECO:
            self.consome(TOKEN.ENDERECO)

    # ---------------------------
    # OpcColchete -> LAMBDA | [ ]
    # ---------------------------
    def OpcColchete(self):
        if self.lexico.tokenLido[0] == TOKEN.ABRECOL:
            self.consome(TOKEN.ABRECOL)
            self.consome(TOKEN.FECHACOL)

    OpcIdentArg = OpcColchete
    OpcIdentDeclar = OpcColchete

    # ---------------------------
    # Corpo -> { ListaDeclar ListaCom }
    # ---------------------------
    def Corpo(self):
        self.consome(TOKEN.ABRECHAVE)
        self.ListaDeclar()
        self.ListaCom()
        self.consome(TOKEN.FECHACHAVE)

    def CompoundStmt(self):
        self.Corpo()

    def Bloco(self):
        self.Corpo()

    # ---------------------------
    # ListaDeclar -> LAMBDA | Declar ListaDeclar
    # ---------------------------
    def ListaDeclar(self):
        while self.lexico.tokenLido[0] in (
            TOKEN.INT,
            TOKEN.FLOAT,
            TOKEN.STRING,
        ):
            self.Declar()

    def Declaration(self):
        self.Declar()

    # ---------------------------
    # Declar -> TipoPrim ident OpcColchete OpcInicializa Listaident ;
    # ---------------------------
    def Declar(self):
        self.TipoPrim()
        self.consome(TOKEN.IDENT)
        self.OpcColchete()
        self.OpcInicializa()
        self.Listaident()
        self.consome(TOKEN.PONTOVIRG)

    # ---------------------------
    # OpcInicializa -> LAMBDA | = Exp
    # ---------------------------
    def OpcInicializa(self):
        if self.lexico.tokenLido[0] == TOKEN.ATRIB:
            self.consome(TOKEN.ATRIB)
            self.Exp()

    # ---------------------------
    # Listaident -> LAMBDA | , ident OpcColchete OpcInicializa Listaident
    # ---------------------------
    def Listaident(self):
        if self.lexico.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.consome(TOKEN.IDENT)
            self.OpcColchete()
            self.OpcInicializa()
            self.Listaident()

    # ---------------------------
    # ListaCom -> LAMBDA | Com ListaCom
    # ---------------------------
    def ListaCom(self):
        while self.lexico.tokenLido[0] in (
            TOKEN.LOOP,
            TOKEN.WHILE,
            TOKEN.FOR,
            TOKEN.IF,
            TOKEN.READ,
            TOKEN.WRITE,
            TOKEN.BREAK,
            TOKEN.CONTINUE,
            TOKEN.RETURN,
            TOKEN.ABRECHAVE,
            TOKEN.INCREM,
            TOKEN.DECREM,
            TOKEN.NOT,
            TOKEN.MAIS,
            TOKEN.MENOS,
            TOKEN.ABREPAR,
            TOKEN.ABRECOL,
            TOKEN.INTNUM,
            TOKEN.FLOATNUM,
            TOKEN.STRINGCONST,
            TOKEN.IDENT,
            TOKEN.PONTOVIRG,
        ):
            self.Com()

    def StmtList(self):
        self.ListaCom()

    # ---------------------------
    # Com -> ComRepete | ComDecisao | ComIO | Exp ; | break ; | continue ; | return OpcExp ; | Bloco
    # ---------------------------
    def Com(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.LOOP:
            self.LoopStmt()
        elif token == TOKEN.WHILE:
            self.WhileStmt()
        elif token == TOKEN.FOR:
            self.ForStmt()
        elif token == TOKEN.IF:
            self.IfStmt()
        elif token in (TOKEN.READ, TOKEN.WRITE):
            self.ComIO()
        elif token == TOKEN.ABRECHAVE:
            self.Bloco()
        elif token == TOKEN.BREAK:
            self.consome(TOKEN.BREAK)
            self.consome(TOKEN.PONTOVIRG)
        elif token == TOKEN.CONTINUE:
            self.consome(TOKEN.CONTINUE)
            self.consome(TOKEN.PONTOVIRG)
        elif token == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.OpcExp()
            self.consome(TOKEN.PONTOVIRG)
        elif token == TOKEN.PONTOVIRG:
            self.consome(TOKEN.PONTOVIRG)
        else:
            self.Exp()
            self.consome(TOKEN.PONTOVIRG)

    def Stmt(self):
        self.Com()

    # ---------------------------
    # ComRepete -> loop Bloco | while ( Exp ) Bloco | for ( RestoComRepete
    # ---------------------------
    def LoopStmt(self):
        self.consome(TOKEN.LOOP)
        self.Bloco()

    def WhileStmt(self):
        self.consome(TOKEN.WHILE)
        self.consome(TOKEN.ABREPAR)
        self.Exp()
        self.consome(TOKEN.FECHAPAR)
        self.Bloco()

    def ForStmt(self):
        self.consome(TOKEN.FOR)
        self.consome(TOKEN.ABREPAR)
        self.RestoComRepete()

    # ---------------------------
    # RestoComRepete -> ident in ident ) Bloco | OpcExp ; OpcExp ; OpcExp ) Bloco
    # ---------------------------
    def RestoComRepete(self):
        if self.lexico.tokenLido[0] == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
            if self.lexico.tokenLido[0] == TOKEN.IN:
                self.consome(TOKEN.IN)
                self.consome(TOKEN.IDENT)
                self.consome(TOKEN.FECHAPAR)
                self.Bloco()
            return
        else:
            if self.lexico.tokenLido[0] == TOKEN.ATRIB:
                self.consome(TOKEN.ATRIB)
                self.Exp()
            else:
                self.RestoFolha()
            self.RestoExp()
            self.consome(TOKEN.PONTOVIRG)
            self.OpcExp()
            self.consome(TOKEN.PONTOVIRG)
            self.OpcExp()
            self.consome(TOKEN.FECHAPAR)
            self.Bloco()
            return
            self.OpcExp()
            self.consome(TOKEN.PONTOVIRG)
            self.OpcExp()
            self.consome(TOKEN.PONTOVIRG)
            self.OpcExp()
            self.consome(TOKEN.FECHAPAR)
            self.Bloco()

    # ---------------------------
    # ComDecisao -> if ( Exp ) Bloco ListaElif ElseOpc
    # ---------------------------
    def IfStmt(self):
        self.consome(TOKEN.IF)
        self.consome(TOKEN.ABREPAR)
        self.Exp()
        self.consome(TOKEN.FECHAPAR)
        self.Bloco()
        self.ListaElif()
        self.ElseOpc()

    # ---------------------------
    # ListaElif -> LAMBDA | elif ( Exp ) Bloco ListaElif
    # ---------------------------
    def ListaElif(self):
        if self.lexico.tokenLido[0] == TOKEN.ELIF:
            self.consome(TOKEN.ELIF)
            self.consome(TOKEN.ABREPAR)
            self.Exp()
            self.consome(TOKEN.FECHAPAR)
            self.Bloco()
            self.ListaElif()

    # ---------------------------
    # ElseOpc -> LAMBDA | else Bloco
    # ---------------------------
    def ElseOpc(self):
        if self.lexico.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.Bloco()

    ElsePart = ElseOpc

    # ---------------------------
    # ComIO -> read ( ident ) ; | write ( ListaExp ) ;
    # ---------------------------
    def ComIO(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.READ:
            self.consome(TOKEN.READ)
            self.consome(TOKEN.ABREPAR)
            self.consome(TOKEN.IDENT)
            self.consome(TOKEN.FECHAPAR)
            self.consome(TOKEN.PONTOVIRG)
        elif token == TOKEN.WRITE:
            self.consome(TOKEN.WRITE)
            self.consome(TOKEN.ABREPAR)
            self.ListaExp()
            self.consome(TOKEN.FECHAPAR)
            self.consome(TOKEN.PONTOVIRG)

    # ---------------------------
    # ListaExp -> Exp RestoListaExp
    # ---------------------------
    def ListaExp(self):
        self.Exp()
        self.RestoListaExp()

    # ---------------------------
    # RestoListaExp -> , Exp RestoListaExp | LAMBDA
    # ---------------------------
    def RestoListaExp(self):
        if self.lexico.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.Exp()
            self.RestoListaExp()

    # ---------------------------
    # OpcExp -> LAMBDA | Zero
    # ---------------------------
    def OpcExp(self):
        token = self.lexico.tokenLido[0]
        if token in (
            TOKEN.INCREM,
            TOKEN.DECREM,
            TOKEN.NOT,
            TOKEN.MAIS,
            TOKEN.MENOS,
            TOKEN.ABREPAR,
            TOKEN.ABRECOL,
            TOKEN.INTNUM,
            TOKEN.FLOATNUM,
            TOKEN.STRINGCONST,
            TOKEN.IDENT,
        ):
            self.Zero()

    OptExpr = OpcExp

    # ---------------------------
    # Exp -> Zero RestoExp
    # ---------------------------
    def Exp(self):
        self.Zero()
        self.RestoExp()

    Expr = Exp

    # ---------------------------
    # RestoExp -> = Zero RestoExp | LAMBDA
    # ---------------------------
    def RestoExp(self):
        if self.lexico.tokenLido[0] == TOKEN.ATRIB:
            self.consome(TOKEN.ATRIB)
            self.Zero()
            self.RestoExp()

    # ---------------------------
    # Zero -> ++ Um | -- Um | Um
    # ---------------------------
    def Zero(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.INCREM:
            self.consome(TOKEN.INCREM)
            self.Um()
        elif token == TOKEN.DECREM:
            self.consome(TOKEN.DECREM)
            self.Um()
        else:
            self.Um()

    # ---------------------------
    # Um -> Dois RestoUm
    # ---------------------------
    def Um(self):
        self.Dois()
        self.RestoUm()

    # ---------------------------
    # RestoUm -> LAMBDA | OR Dois RestoUm
    # ---------------------------
    def RestoUm(self):
        if self.lexico.tokenLido[0] == TOKEN.OR:
            self.consome(TOKEN.OR)
            self.Dois()
            self.RestoUm()

    # ---------------------------
    # Dois -> Tres RestoDois
    # ---------------------------
    def Dois(self):
        self.Tres()
        self.RestoDois()

    # ---------------------------
    # RestoDois -> LAMBDA | AND Tres RestoDois
    # ---------------------------
    def RestoDois(self):
        if self.lexico.tokenLido[0] == TOKEN.AND:
            self.consome(TOKEN.AND)
            self.Tres()
            self.RestoDois()

    # ---------------------------
    # Tres -> NOT Tres | Quatro
    # ---------------------------
    def Tres(self):
        if self.lexico.tokenLido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.Tres()
        else:
            self.Quatro()

    # ---------------------------
    # Quatro -> Cinco Resto4
    # ---------------------------
    def Quatro(self):
        self.Cinco()
        self.RestoQuatro()

    # ---------------------------
    # Resto4 / RestoQuatro -> > Cinco | >= Cinco | < Cinco | <= Cinco | == Cinco | != Cinco | LAMBDA
    # ---------------------------
    def RestoQuatro(self):
        if self.lexico.tokenLido[0] == TOKEN.OPREL:
            self.consome(TOKEN.OPREL)
            self.Cinco()
            self.RestoQuatro()

    def Resto4(self):
        self.RestoQuatro()

    # ---------------------------
    # Cinco -> Seis RestoCinco
    # ---------------------------
    def Cinco(self):
        self.Seis()
        self.RestoCinco()

    # ---------------------------
    # RestoCinco -> LAMBDA | + Seis RestoCinco | - Seis RestoCinco
    # ---------------------------
    def RestoCinco(self):
        token = self.lexico.tokenLido[0]
        if token in (TOKEN.MAIS, TOKEN.MENOS):
            self.consome(token)
            self.Seis()
            self.RestoCinco()

    # ---------------------------
    # Seis -> Sete RestoSeis
    # ---------------------------
    def Seis(self):
        self.Sete()
        self.RestoSeis()

    # ---------------------------
    # RestoSeis -> LAMBDA | * Sete RestoSeis | / Sete RestoSeis | div Sete RestoSeis | mod Sete RestoSeis
    # ---------------------------
    def RestoSeis(self):
        token = self.lexico.tokenLido[0]
        if token in (TOKEN.MULT, TOKEN.DIVIDE, TOKEN.DIV, TOKEN.MOD):
            self.consome(token)
            self.Sete()
            self.RestoSeis()

    # ---------------------------
    # Sete -> + Sete | - Sete | Folha
    # ---------------------------
    def Sete(self):
        token = self.lexico.tokenLido[0]
        if token in (TOKEN.MAIS, TOKEN.MENOS):
            self.consome(token)
            self.Sete()
        else:
            self.Folha()

    # ---------------------------
    # Folha -> valorInt | valorFloat | valorString | ValorLista | ( Zero ) | ident RestoFolha
    # ---------------------------
    def Folha(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.ABREPAR:
            self.consome(TOKEN.ABREPAR)
            self.Zero()
            self.consome(TOKEN.FECHAPAR)
        elif token == TOKEN.INTNUM:
            self.consome(TOKEN.INTNUM)
        elif token == TOKEN.FLOATNUM:
            self.consome(TOKEN.FLOATNUM)
        elif token == TOKEN.STRINGCONST:
            self.consome(TOKEN.STRINGCONST)
        elif token == TOKEN.ABRECOL:
            self.ValorLista()
        elif token == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
            self.RestoFolha()
        else:
            raise Exception(
                f"Erro Sintático na linha {self.lexico.linha}: Expressão ou folha esperada, veio {TOKEN.msg(token)}"
            )

    # ---------------------------
    # RestoFolha -> LAMBDA | [ Zero ] | ( ListaParam )
    # ---------------------------
    def RestoFolha(self):
        token = self.lexico.tokenLido[0]
        if token == TOKEN.ABRECOL:
            self.consome(TOKEN.ABRECOL)
            self.Zero()
            self.consome(TOKEN.FECHACOL)
        elif token == TOKEN.ABREPAR:
            self.consome(TOKEN.ABREPAR)
            self.ListaParam()
            self.consome(TOKEN.FECHAPAR)

    # ---------------------------
    # ListaParam -> LAMBDA | Param RestoListaParam
    # ---------------------------
    def ListaParam(self):
        token = self.lexico.tokenLido[0]
        if token in (
            TOKEN.INCREM,
            TOKEN.DECREM,
            TOKEN.NOT,
            TOKEN.MAIS,
            TOKEN.MENOS,
            TOKEN.ABREPAR,
            TOKEN.ABRECOL,
            TOKEN.INTNUM,
            TOKEN.FLOATNUM,
            TOKEN.STRINGCONST,
            TOKEN.IDENT,
        ):
            self.Param()
            self.RestoListaParam()

   
    # Param -> Zero
    
    def Param(self):
        self.Zero()

    # RestoListaParam -> , Param RestoListaParam | LAMBDA
    def RestoListaParam(self):
        if self.lexico.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.Param()
            self.RestoListaParam()

    def Params(self):
        self.ListaParam()

     
    # ValorLista -> [ ListaParam ]
   
    def ValorLista(self):
        self.consome(TOKEN.ABRECOL)
        self.ListaParam()
        self.consome(TOKEN.FECHACOL)

    def parse(self):
        try:
            self.inicio()
            print("correto")
        except Exception as e:
            print(f"Erro sintático : {e}")

if __name__ == "__main__":

    caminho = r"/home/lucas/Área de trabalho/compilador1C/teste.txt"

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            # Inicializa o analisador léxico passando o arquivo aberto
            lexico = Lexico(arquivo)

            # Inicializa e executa o analisador sintático 
            sintatico = Sintatico(lexico)
            sintatico.parse()

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")