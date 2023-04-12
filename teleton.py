from pyrogram import Client, types
from pyrogram.utils import compute_password_check
from pyrogram.types import ChatPrivileges
from pyrogram.raw import functions, types
from collections import OrderedDict

class Teleton:
    def __init__(self, api_id, api_hash, username, passwd_bot):
        self.api_id = api_id
        self.api_hash = api_hash
        self.username = username
        self.password = passwd_bot

    def createChannels(self, title, group_title, answer):
        try:
            with Client("sessions/user"+str(self.api_id), self.api_id, self.api_hash) as app:
                about = ""

                handleChannel = app.invoke(functions.channels.CreateChannel(title=title, about=about, broadcast=True))
                handleChat = app.invoke(functions.channels.CreateChannel(title=group_title, about=about, broadcast=True, megagroup=True))   

                dataChats = OrderedDict([
                    ("channel",
                        OrderedDict([
                            ("id", handleChannel.chats[0].id),
                            ("hash", handleChannel.chats[0].access_hash),
                            ("chat_id", int('-100'+str(handleChannel.chats[0].id)))]),
                        ),
                    ("group",
                        OrderedDict([
                            ("id", handleChat.chats[0].id),
                            ("hash", handleChat.chats[0].access_hash),
                            ("chat_id", int('-100'+str(handleChat.chats[0].id)))])
                        )
                    ]);

                app.invoke(functions.channels.SetDiscussionGroup(broadcast=types.InputChannel(channel_id=dataChats['channel']['id'], access_hash=dataChats['channel']['hash']), group=types.InputChannel(channel_id=dataChats['group']['id'], access_hash=dataChats['group']['hash'])))

                rules = ChatPrivileges(can_manage_chat=True,can_delete_messages=True,can_manage_video_chats=True,can_restrict_members=True,can_promote_members=True,can_change_info=True,can_post_messages=True,can_edit_messages=True,can_invite_users=True,can_pin_messages=True,is_anonymous=True)

                app.promote_chat_member(dataChats['channel']['chat_id'], "@TeletonChatBot", rules)
                app.promote_chat_member(dataChats['group']['chat_id'], "@TeletonChatBot", rules)
                app.promote_chat_member(dataChats['channel']['chat_id'], self.username, rules)
                app.promote_chat_member(dataChats['group']['chat_id'], self.username, rules)

                answer.put(self.status(200, {'channelId': dataChats['channel']['chat_id'], 'groupId': dataChats['group']['chat_id']}))
        except Exception as error:
            if str(error) == "database is locked":
                answer.put(self.status(300, {'wait': 'This process is busy, try again in a few seconds'}))
            else:
                answer.put(self.status(400, {'error': str(error)}))

    def editAdmin(self, channel_id, group_id, answer):
        try:
            with Client("sessions/user"+str(self.api_id), self.api_id, self.api_hash) as app:
                app.invoke(functions.channels.EditCreator(channel= app.resolve_peer(channel_id), user_id= app.resolve_peer(self.username), password=compute_password_check(app.invoke(functions.account.GetPassword()),password=self.password)))
                app.invoke(functions.channels.EditCreator(channel= app.resolve_peer(group_id), user_id= app.resolve_peer(self.username), password=compute_password_check(app.invoke(functions.account.GetPassword()),password=self.password)))
                app.leave_chat(channel_id)
                app.leave_chat(group_id, delete=False)
                answer.put(self.status(200, 'success'))
        except Exception as error:
            if str(error) == "database is locked":
                answer.put(self.status(300, {'wait': 'This process is busy, try again in a few seconds'}))
            else:
                answer.put(self.status(400, {'error': str(error)}))

    def status(self, code, data):
        if code == 200:
            return {'status': True, 'code': code, 'data': data}
        return {'status': False, 'code': code, 'data': data}