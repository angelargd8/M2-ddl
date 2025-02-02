%{
#include <cstdlib>
#include <string>
#include "y.tab.h"

void yyerror(const char *s);

%}

%%

[a-zA-Z][a-zA-Z0-9]*    { yylval.str = new std::string(yytext);  return ID; }
[0-9]+(\.[0-9]+)?    { yylval.num = atof(yytext); return NUMBER; }
"+"                     { return '+'; }
"-"                     { return '-'; }
"*"                     { return '*'; }
"/"                     { return '/'; }
"="                     { return '='; }
":"                     { return ':'; }
"("                     { return '('; }
")"                     { return ')'; }
[ \t\n]                   ;  // skip whitespace
.                       {  return yytext[0]; }

%%

int yywrap() {
    return 1;
}