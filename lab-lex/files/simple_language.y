%{
#include <iostream>
#include <string>
#include <map>
static std::map<std::string, int> vars;
inline void yyerror(const char *str) { std::cout << str << std::endl; }
int yylex();
%}

%union { int num; std::string *str; }

%token<num> NUMBER
%token<str> ID
%type<num> expression
%type<num> assignment

%left '='
%right '+' '-'
%right '*' '/'

%%

program : statement_list
        | error { yyerror("Error: Token inválido"); }
        ;

statement_list: statement
    | statement_list statement
    ;

statement: assignment
    | expression ':'          { std::cout << $1 << std::endl; }
    ;

assignment : ID '=' expression
            {
                std::cout << "Assign " << *$1 << " = " << $3 << std::endl;
                vars[*$1] = $3;
                delete $1;
            }
            ;


expression: NUMBER                  { $$ = $1; }
            | ID                      { $$ = vars[*$1]; delete $1; }
            | expression '+' expression     { $$ = $1 + $3; std::cout << "Suma: " << $1 << " + " << $3 << std::endl; }
            | expression '-' expression     { $$ = $1 - $3; std::cout << "Resta: " << $1 << " - " << $3 << std::endl; }
            | expression '*' expression     { $$ = $1 * $3; std::cout << "Multiplicación: " << $1 << " * " << $3 << std::endl; }
            | expression '/' expression     { $$ = $1 / $3; std::cout << "División: " << $1 << " / " << $3 << std::endl; }
            ;

%%

int main() {
    yyparse();
    return 0;
}