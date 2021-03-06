from enum import unique, auto, Enum
from typing import Dict
#set($request = "")
#set($comment = '# noqa')
#set($sc = ${StringUtils.removeUnderScores($service)})
#set($ns = $requests.replace(" ", ""))
#set($rl = $ns.split(","))
#set($rm = {})
#set($cl = "")
#set($i = 0)
#foreach($request in $rl)
    #set($rm[$request] = {})
    #set($rm[$request].lower = $request.toLowerCase())
    #set($rm[$request].upper = $request.toUpperCase())
    #set($rm[$request].camel = ${StringUtils.removeUnderScores($request)})
    #set($cl = "${cl}${rm[$request].camel}")
    #set($i = $i + 1)
    #if($i < $rl.size())
        #set($cl = "${cl}, ")
    #end
#end##

#foreach($request in $rm)
from ${request.lower} import ${request.camel}
#end##

from router import Route, route
from view import View

@unique
class ${sc}Request(Enum):
#foreach($request in $rm)
        ${request.upper} = auto()
#end

# TODO: Update route output (Callable/default=View.generic)
#  example: output=Lambda value: View.construct(.. ResponseField: value[data]
routes: Dict[Enum, Route] = {
#foreach($request in $rm)
    ${sc}Request.${request.upper}: Route(${request.camel}, View.generic),
#end
}


@route(routes, ${sc}Request)
def lambda_handler(event, context):  ${comment}
    pass
