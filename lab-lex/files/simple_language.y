%{
#include <iostream>
#include <string>
#include <map>
#include <cstdlib>
extern char *yytext;
extern int yylineno;

static std::map<std::string, double> vars;
inline void yyerror(const char *str) { std::cout << str << std::endl; }
int yylex();
%}

%union { double num; std::string *str; }

%token<num> NUMBER
%token<str> ID
%type<num> expression
%type<num> assignment

%right '='
%left '+' '-'
%left '*' '/'
%nonassoc UNARY

%%

program: statement_list
        ;

statement_list: statement
    | statement_list statement
    ;

statement: assignment
    | expression ':'          { std::cout << $1 << std::endl; }
    ;

assignment: ID '=' expression
    { 
        printf("Assign %s = %f\n", $1->c_str(), $3);
        $$ = vars[*$1] = $3; 
        delete $1;
    }
    ;

expression: NUMBER                  { $$ = $1; }
    | '-' expression %prec UNARY    { $$ = -$2 ; }
    | ID                            { $$ = vars[*$1];      delete $1; }
    | expression '+' expression     { $$ = $1 + $3; }
    | expression '-' expression     { $$ = $1 - $3; }
    | expression '*' expression     { $$ = $1 * $3; }
    | expression '/' expression     { $$ = $1 / $3; }
    | '(' expression ')'     { $$ = $2 ; }

    ;

%%

int main() {
    yyparse();
    return 0;
}

void yyerror(const char *s){
    std::cerr << "error: " << s << " en el token '" << yytext << "' en linea " << yylineno << std::endl;
}