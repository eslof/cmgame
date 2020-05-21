#set($request = "")
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
    from .${request.lower} import ${request.camel}
#end##


@unique
class ${sc}Request(Enum):
#foreach($request in $rm)
        ${request.upper} = auto()
#end

# TODO: Update route output (Callable/default=View.generic)
#  example: output=Lambda value: View.construct(.. ResponseField: value[data]
routes: ROUTES_TYPE = {
#foreach($request in $rm)
    ${sc}Request.${request.upper}: Route(${request.camel}, View.generic),
#end
}


@route(routes, ${sc}Request)
def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    pass