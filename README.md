# PythonSCL
Implementation of SCL Interpreter in Python

* [Syntax Rules](#syntax-rules)
* [Lexical Rules](#lexical-rules)

## Syntax Rules

```
start : symbols forward_refs specifications globals implement
      ;

symbols :
        | symbols symbol_def
        ;

symbol_def : SYMBOL IDENTIFIER HCON
           ;

forward_refs :
             | FORWARD frefs
             ;

frefs  : REFERENCES forward_list
       | forward_list
       ;

forward_list : forwards 
             | forward_list forwards
             ;

forwards : 
         | check_ext func_main dec_parameters
         ;

check_ext :
          | MEXTERN 
          ;

func_main : 
          | FUNCTION IDENTIFIER oper_type 
          | MAIN {dec_main();}
          ;

oper_type : RETURN chk_ptr chk_array ret_type 
          ;

chk_ptr :
        | POINTER {pointer_flag = true;}
        ;

chk_array :
          | ARRAY array_dim_list
          ;

array_dim_list : LB array_index RB
               | array_dim_list LB array_index RB 
               ;

array_index : IDENTIFIER 
            | ICON 
            ;

ret_type  : TYPE type_name 
          | STRUCT IDENTIFIER 
          | STRUCTYPE IDENTIFIER 
          ;

type_name       : MVOID
                | INTEGER
                | SHORT
                | REAL
                | FLOAT
                | DOUBLE
                | TBOOL
                | CHAR
                | TSTRING OF LENGTH ICON 
                | TBYTE
                ;

specifications  :
                | SPECIFICATIONS spec_list
                ;

spec_list : spec_def
          | spec_list spec_def
          ;

spec_def : ENUM 
         | STRUCT 
         ;

globals : 
        | GLOBAL declarations 
        ;

declarations : 
             | DECLARATIONS
             ;

implement : IMPLEMENTATIONS funct_list
          ;

funct_list : funct_def
           | funct_list funct_def
           ;

funct_def : funct_body
          ;

funct_body: FUNCTION main_head parameters f_body
          ;

main_head : MAIN 
          | IDENTIFIER
          ;

parameters : 
           | PARAMETERS param_list
           ;

param_list : param_def
           | param_list COMMA param_def 
           ;

param_def : identifier chk_const chk_ptr chk_array OF TYPE type_name
          ;

chk_const :
          | CONSTANT 
          ;

f_body : BEGIN <statement_list> ENDFUN
       ;

statement_list : statement 
               | statement_list statement
               ;

statement : if_statement
          | assignment_statement
          | while_statement
          | print_statement
          | repeat_statement
          ;

if_statement : IF boolean_expression THEN statement_list 
               ELSE statement_list ENDIF
             ;

while_statement : WHILE boolean_expression DO statement_list ENDWHILE
                ;

assignment_statement : LET identifier assignment_operator arithmetic_expression
                     ;

repeat_statement : REPEAT statement_list UNTIL boolean_expression ENDREPEAT
                 ;

print_statement : DISPLAY arg_list
                ;

arg_list : args
         | arg_list comma args
         ;

args : identifier
     | constant
     | string
     ;

boolean_expression : arithmetic_exp relative_op arithmetic_exp
                   ;

relative_op : le_operator 
            | lt_operator 
            | ge_operator 
            | gt_operator 
            | eq_operator 
            | ne_operator
            ;

arithmetic_exp : arithmetic_exp add_operator mulexp
               | arithmetic_exp sub_operator mulexp
               | mulexp 
               ;

mulexp : mulexp mul_operator primary
       | mulexp div_operator primary
       | primary
       ;

primary : left_paren  arithmetic_exp right_paren
        | minus primary
        | constant
        | identifier
        ;
```

## Lexical Rules
```
identifier → letter char_list
char_list → letter_digit char_list
           | letter_digit
literal_integer → digit literal_integer
                 | digit
assignment_operator → =
le_operator → <= 
lt_operator → < 
ge_operator → >= 
gt_operator → >
eq_operator → ==
ne_operator → ~=
add_operator → +
sub_operator → -
mul_operator → *
div_operator → / 
