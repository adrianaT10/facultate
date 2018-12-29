%%

%class Flexer
%unicode
/*%debug*/
%int
%line
%column

%{

    Graph graph = new Graph();
    String context;
    String transContext = "";
    String source, destination;
    char input_letter;
%}

LineTerminator = \r|\n|\r\n
WS = {LineTerminator} | [ \t\f]
special =  "!"|"#"|"$"|"%"|"&"|"-"|"."|"/"|":"|";"|"<"|">"|"="|"@"|"["|"]"|"^"|"`"|"~"|"_"|"'"|"*"|"+"|"?"|"|"
lower = [a-z]
upper = [A-Z]

stare = ({upper}|{lower}|[:digit:]|"_")+

letter_alpha = {lower} | {upper} | {special} | [:digit:]

word = {letter_alpha}+{WS}*

anything = {letter_alpha}|"{"|"}"|","|"("|")"


%state STATE SEP SEPS SEPA SEPT SEPF CHARA STATET STATEI STATEF WORD ERROR DONTH

%%

{WS}	{/*Skip whitespace in any state*/}

<YYINITIAL>"({" {
	  context = "STATES";
	  yybegin(STATE);
	}


<STATE>{stare} {
	graph.addNode(yytext());
	yybegin (SEPS);
}

<SEPS> {
	"," {yybegin(STATE);}
	"}" {
      yybegin(SEP);
	}
}

<SEP> {
	"," {
	  if(context.equals("TRANSITIONS")) {
	    context = "INITIAL_STATE";
	    yybegin(STATEI);
	  } else {
	    yybegin(ERROR);
	  }
	}
	",{" {
	  if(context.equals("STATES")) {
	    context = "ALPHABET";
	    yybegin(CHARA);
	  } else if(context.equals("INITIAL_STATE")) {
	    context = "FINAL_STATE";
	    yybegin(STATEF);
	  }  else {
	    yybegin(ERROR);
	  }
	}
	",(" {
	  context = "TRANSITIONS";
	  yybegin(SEPT);
	}
}

<CHARA>{letter_alpha} {
    if(context.equals("ALPHABET")) {
      String symbol = yytext();
	  graph.addToAlphabet(symbol.charAt(0));
	  yybegin(SEPA);
	} else if(context.equals("TRANSITIONS")) {
	  String symbol = yytext();
      input_letter = symbol.charAt(0);
	  yybegin(SEPT);
	} else {
	    yybegin(ERROR);
	  }
}

<SEPA> {
	","  {yybegin(CHARA);}
	"}"  {yybegin(SEP);}
}

<SEPT> {
	"d("  {
      transContext = "SOURCE_NODE";
	  yybegin(STATET);
	}
	",d("  {
      transContext = "SOURCE_NODE";
	  yybegin(STATET);
	}
	"," {
	  if(transContext == "SOURCE_NODE") {
	    yybegin(CHARA);
	  } else {
	    yybegin(ERROR);
	  }
	}
	")=" {
	  transContext = "DEST_NODE";
	  yybegin(STATET);
	}
	")" {
	  if(transContext.equals("DEST_NODE")) { /* s-a ajuns la sf tranzitiilor*/
        yybegin(SEP);
	  } else {
	    yybegin(ERROR);
	  }
	}
}

<STATET> {
	{stare} {
	  if(transContext.equals("SOURCE_NODE")) {
        source = yytext();
        yybegin(SEPT);
	  }
	  if(transContext.equals("DEST_NODE")) {
        graph.addTransition(source, input_letter, yytext());
        yybegin(SEPT);
	  }
	}
}

<STATEI>{stare} {
	graph.setInitialState(yytext());
	yybegin(SEP);
}

<SEPF> {
  "," {yybegin(STATEF);}
  "})" {}
}

<STATEF> {
	{stare}  {
	   graph.setFinalState(yytext());
	   yybegin(SEPF);
	   }
	"})"  {}
}

<WORD> {
    {word} {
        graph.verifyWord(yytext());
        }
    ","  {}
    "{"  {}
    "}"  {}
}

<ERROR>{anything} {
    graph.foundSyntaxError();
    yybegin(DONTH);
  }
<DONTH>{anything} {}
{anything} {
  yybegin(ERROR);}

