grammar Cymbol;



//Lexer
fragment NUMBER    : [0-9];
fragment LETTER    : [a-zA-Z];
fragment UNDERLINE : '_';
//modificado abaixo
fragment LETTERASP : '"'.*?'"';
fragment BOOL : [0-1]|'true'|'false';
fragment FLOATNUMBER : [0-9]+'.'[0-9]+;

TYPEINT  : 'int';
TYPEVOID : 'void';
//modificado abaixo
TYPEBOOLEAN : 'boolean';
TYPESTRING : 'string';
TYPEFLOAT : 'float';

IF     : 'if';
ELSE   : 'else';
RETURN : 'return';

LP        : '(';
RP        : ')';
COMMA     : ',';
SEMICOLON : ';';
LB        : '{';
RB        : '}';

AS    : '=';
EQ    : '==';
NE    : '!=';
NOT   : '!';
GT    : '>';
LT    : '<';
GE    : '>=';
LE    : '<=';
MUL   : '*';
DIV   : '/';
PLUS  : '+';
MINUS : '-';
//modificado abaixo
OR    : '||';
AND   : '&&';

ID  : (UNDERLINE | LETTER) (UNDERLINE | LETTER | NUMBER)*;
INT : NUMBER+;
//modificado abaixo 
BOOLEAN : BOOL;
STRING : LETTERASP;
FLOAT : FLOATNUMBER+;

BLOCKCOMMENT : '/*' .*? '*/' -> skip;
LINECOMMENT  : '//' .*? '\n' -> skip;
WS           : [ \t\n\r]+ -> skip;



//Parser
fiile : (funcDecl | varDecl)+ EOF?
      ;

varDecl : tyype ID ('=' expr)? ';'
        ;

tyype : TYPEINT                 #FormTypeInt              
      | TYPEVOID                #FormTypeVoid          
      | TYPEBOOLEAN             #FormTypeBoolean                 
      | TYPESTRING              #FormTypeString
      | TYPEFLOAT               #FormTypeFloat                 
      ;

funcDecl : tyype ID '(' paramTypeList? ')' block
         ;

paramTypeList : paramType (',' paramType)*
              ;

paramType : tyype ID
          ;

block : '{' stat* '}'
      ;

assignStat : ID '=' expr ';'
           ;

returnStat : 'return' expr? ';' 
           ;

ifElseStat : ifStat (elseStat)?
           ;

ifElseExprStat : block 
               | ifElseStat
               | returnStat
               | assignStat
               | exprStat
               ;

exprStat : expr ';'
         ;

exprList : expr (',' expr)*
         ;

ifStat : 'if' '(' expr ')' ifElseExprStat       #ifStatmentCall
       ;

elseStat : 'else' ifElseExprStat
         ;

stat : varDecl
     | ifElseStat
     | returnStat
     | assignStat
     | exprStat
     ;

expr : ID '(' exprList? ')'                             #FunctionCallExpr
     | op=('+' | '-') expr                              #SignedExpr
     | '!' expr                                         #NotExpr
     | expr op=('<' | '>' | '<=' | '>=') expr           #ComparisonExpr
     | expr op=('*' | '/') expr                         #MulDivExpr
     | expr op=('+' | '-') expr                         #AddSubExpr
     | expr op=('==' | '!=') expr                       #EqExpr
     | ID                                               #VarIdExpr
     | INT                                              #IntExpr
     | '(' expr ')'                                     #ParenExpr
     | BOOLEAN                                          #BooleanExpr
     | expr op=('||' | '&&') expr                       #OrAndExpr
     | FLOAT                                            #FloatExpr
     | STRING                                           #StringExpr
     ;

