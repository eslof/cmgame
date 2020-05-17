from default_imports import *
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

assert_inheritance([${cl}], RequestHandler)


@unique
class ${sc}Request(Enum):
#foreach($request in $rm)
        ${request.upper} = auto()
#end


routes = {
#foreach($request in $rm)
    ${sc}Request.${request.upper}: Route(${request.camel}, View.generic),
#end
}


def lambda_handler(event, context):
    """Return of 'handler.validate()' is passed to 'handler.run()'.
    Finally the return value of 'handler.run()' is passed to associated 'route.output()'."""

    user_id = User.validate_id(event)
    req = validate_request(event, ${sc}Request)

    with routes[req] as route:
        handler = route.handler
        output = route.output

    valid_data = handler.validate(event, user_id)
    output(handler.run(event, user_id, valid_data))
