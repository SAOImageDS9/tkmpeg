%{
%}

#include coordsys.tin
#include wcssys.tin
#include yesno.tin
#include numeric.tin
#include string.tin

%start command

%token AXIS_
%token AXES_
%token CLOSE_
%token FIRST_
%token INTERVAL_
%token LAST_
%token LOCK_
%token MATCH_
%token NEXT_
%token NONE_
%token OPEN_
%token ORDER_
%token PLAY_
%token PREV_
%token STOP_

%token 123_
%token 132_
%token 213_
%token 231_
%token 312_
%token 321_

%%

#include coordsys.trl
#include wcssys.trl
#include yesno.trl
#include numeric.trl

command : cube 
 | cube {yyclearin; YYACCEPT} STRING_
 ;

cube : OPEN_
 | CLOSE_ {CubeDestroyDialog}
 | MATCH_ matchslice {MatchCubeCurrent $2}
 | LOCK_ lockslice {ProcessCmdSet cube lock $2 LockCubeCurrent}
 | PLAY_ {CubePlay}
 | STOP_ {CubeStop}
 | NEXT_ {CubeNext}
 | PREV_ {CubePrev}
 | INTERVAL_ numeric {ProcessCmdSet cube interval [expr int($2*1000)]}
 | AXIS_ INT_ {ProcessCmdSet cube axis [expr $2-1]}
 | AXES_ order
 | ORDER_ order
 | INT_ {CubeCmdCoord $1 image 2}
 | numeric wcssys {CubeCmdCoord $1 $2 2}
 | numeric wcssys INT_ {CubeCmdCoord $1 $2 [expr $3-1]}
 ;

order : LOCK_ yesno {ProcessCmdSet cube lock,axes $2 LockAxesCurrent}
 | orderAxes {ProcessCmdSet cube axes $1}
 ;

orderAxes : 123_ {set _ 123}
 | 132_ {set _ 132}
 | 213_ {set _ 213}
 | 231_ {set _ 231}
 | 312_ {set _ 312}
 | 321_ {set _ 321}
 ;

lockslice : {set _ image}
 | IMAGE_ {set _ image}
 | wcssys {set _ $1}
 | NONE_ {set _ none}
 ;

matchslice : IMAGE_ {set _ image}
 | wcssys {set _ $1}
 ;

%%

proc cube::yyerror {msg} {
     variable yycnt
     variable yy_current_buffer
     variable index_

     ParserError $msg $yycnt $yy_current_buffer $index_
}
