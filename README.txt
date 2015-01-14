Server accepts JSON encoded messages on /chat websocket


Each message should have 'type' field


There are following types of messages that are accepted by server

- auth
- add_group
- rm_group
- game_start
- game_stop
- message


* auth
Login user and set his login name

Expectin one more field - login

Example:

{"type":"auth",
 "login":"nickname"}

* add_group, rm_group

Add current user to the group, remove current user from the group.

Invalid request is noop

User can't be added if group already have 4 members, or game for that group already started.

Expecting one additional field group

{"type":"add_group",
 "group":"nickname"}


* game_start, game_stop

Mark/unmark some group as started game. After that there can't be new users added to that group.

{"type":"game_start",
 "group":"nickname"}


* message

Message that would be broadcasted to some group.
User can send message only to groups he is member of.

Expecting fields group,data

{"type":"message",
 "group":"nickname"
 "data": { "some_field":"contents}

}


Messages that are sent by server.
JSON formatted messages with mandatory field "type"


- message
When somebody sends a message it broadcasted to all members of group except author

Example

{"type":"message",
 "data": { "some_field":"contents},
 "user": "nickname"

}


- group_info
Currently send only once after login.

Contains list of one member groups ( Each logged in user have one group named after him)

Example:

{"type": "group_info",
"free" : ["another_nickname"]
}
