#Original lib from https://github.com/herywinarto/SIMPLE-PROTECTV2, Rebuild by Alif Budiman Wahabbi
#---------- Copyright 2021 by Alif Budiman Wahabbi, find me on Instagram: alifbudimanwahabbi
#------------------------------------------------------------- Line: alifbudimanwahabbi
from alipmodule import * #import module
#login account
alip = ALIP_LINE(myToken="YOUR TOKEN", #  <--- imput your token here
            myApp="ANDROIDLITE\t2.14.0\tAndroid OS\t5.1.1")
#data
ALIPmid = alip.profile.mid
creator = [""] #imput your mid here
owner = [""] #imput your mid here
Bots = []
Blacklist = []
ongoingbc = []
waitinglist = []
Blgroup = []
groupnow = []

with open("datagame.json", "r", encoding="utf_8_sig") as f:
    itu = json.loads(f.read())
    datagame = itu
with open("databot.json", "r", encoding="utf_8_sig") as f:
    ini = json.loads(f.read())
    databot = ini

wait = {
    "keyCmd":"",
    "setKey":True,
}

#definision
def AddBlacklist(target):
    if target not in Blacklist:
        Blacklist.append(target)
    else:pass

def AddBlacklistGC(group):
    if group not in Blgroup:
        Blgroup.append(group)
    else:pass

def inviteSquad(group):
    group = alip.getChats([group]).chats[0]
    mems = list(group.extra.groupExtra.memberMids)
    pends = list(group.extra.groupExtra.inviteeMids)
    ls = []
    for x in Bots:
        if x not in pends and x not in mems:
            ls.append(x)
    if ls == []:
        pass
    else:
        if ls != []:
            alip.inviteIntoChat(group, ls)

def restartBot():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def command(text):
    pesan = text.lower()
    if pesan.startswith(wait["keyCmd"]):
        cmd = pesan.replace(wait["keyCmd"], "")
    else:
        cmd = "command"
    return cmd

def removeCmd(cmd, text):
	key = wait["keyCmd"]
	if wait["setKey"] == False: key = ''
	rmv = len(key + cmd) + 1
	return text[rmv:]

def sendMentionv2(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@alip<x>fxg "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    alip.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def super_mention(to,status,text, dataMid=[], pl='', ps='',pg='',pt=[]):
    arr = []
    list_text=ps
    i=0
    no=pl
    if pg == "DeleteBlacklist":
        for l in dataMid:
            try:
                Blacklist.remove(l)
            except:
                continue
            no+=1
            if no == len(pt):list_text+='\n'+str(no)+'. @[wew-'+str(i)+'] '
            else:list_text+='\n'+str(no)+'. @[wew-'+str(i)+'] '
            i=i+1
        text=list_text
    if pg == "DeleteWhitelist":
        for l in dataMid:
            try:
                Bots.remove(l)
            except:
                continue
            no+=1
            if no == len(pt):list_text+='\n'+str(no)+'. @[wew-'+str(i)+'] '
            else:list_text+='\n'+str(no)+'. @[wew-'+str(i)+'] '
            i=i+1
        text=list_text
    i=0
    for l in dataMid:
        if l not in ALIPmid:
            mid=l
            name='@[wew-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int( ln_text.index(name) )
                line_e=(int(line_s)+int( len(name) ))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
    alip.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def backupData():
    try:
        backup = databot
        f = codecs.open('databot.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = datagame
        f = codecs.open('datagame.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        print(error)
        return False
#bot
def worker(op):
    global time
    global ast
    global Blacklist
    global Bots
    global AddBlacklistGC
    global totalcount
    group = op.param1
    executor = op.param2
    try:
        if op.type == 0:
            return
#====================================================================== INVITE
        if op.type == 13 or op.type == 124:
            if ALIPmid in op.param3:
                if op.param2 not in creator:
                    group = alip.getChats([op.param1]).chats[0]
                    mems = list(group.extra.groupExtra.memberMids)
                    name = alip.getContact(op.param2).displayName
                    if len(mems) > 49:
                        if op.param2 not in datagame['info']:
                            datagame['name'][name] =  {"point":1}
                            datagame['info'][op.param2] =  '%s' % name
                            if op.param1 not in Blgroup:
                                alip.acceptChatInvitation(op.param1)
                                sendMentionv2(op.param1, "@! Thanks for Invite me, you get 1 ticket",[op.param2])
                            else:
                                alip.acceptChatInvitation(op.param1)
                                alip.sendMessage(op.param1, "This Groupn Added to Blacklist\nType 'Chat owner <message>'")
                                alip.deleteSelfFromChat(op.param1)
                        else:
                            alip.acceptChatInvitation(op.param1)
                            sendMentionv2(op.param1, "@! Thanks for Invite me, you get 1 ticket",[op.param2])
                            datagame['name'][datagame['info'][op.param2]]["point"] += 1
                    else:
                        alip.acceptChatInvitation(op.param1)
                        alip.sendMessage(op.param1, "Minimum Group 50 Members")
                        alip.deleteSelfFromChat(op.param1)
                else:
                    alip.acceptChatInvitation(op.param1)
                    alip.sendMessage(op.param1, "Hai mastah")
            else:pass
            backupData()
#====================================================================== KICK
        if op.type == 19 or op.type == 133:
            if op.param3 in ALIPmid:
                if op.param2 not in Bots and op.param2 not in owner:
                    try:
                        AddBlacklist(op.param2)
                        AddBlacklistGC(op.param1)
                    except:pass
#=======================================================================CANCEL
        if op.type == 32 or op.type == 126:
            if op.param3 in ALIPmid:
                if op.param2 not in Bots and op.param2 not in owner:
                    try:
                        AddBlacklist(op.param2)
                        AddBlacklistGC(op.param1)
                    except:pass

        if op.type == 25 or op.type == 26:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                msg._from = msg._from
                if msg.toType == 0 or msg.toType == 2:
                    if msg.toType == 0:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 1:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help admin":
                                cooms = str(wait["keyCmd"])
                                if (
                                    msg._from in creator
                                    or msg._from in owner
                                    or msg._from in Bots
                                ):
                                    txt = "<< Help Commands >>\n\n"
                                    txt += "\n⌖ "+cooms+"addbot <tag>"
                                    txt += "\n⌖ "+cooms+"banlist"
                                    txt += "\n⌖ "+cooms+"botlist"
                                    txt += "\n⌖ "+cooms+"clearbot"
                                    txt += "\n⌖ "+cooms+"clearban"
                                    txt += "\n⌖ "+cooms+"delban <num> or/w <-/,>"
                                    txt += "\n⌖ "+cooms+"delbot <num> or/w <-/,>"
                                    txt += "\n⌖ "+cooms+"addme"
                                    txt += "\n⌖ "+cooms+"speed"
                                    txt += "\n⌖ "+cooms+"grouplist"
                                    txt += "\n⌖ "+cooms+"pendinglist"
                                    txt += "\n⌖ "+cooms+"joinall pending"
                                    txt += "\n⌖ "+cooms+"out"
                                    txt += "\n⌖ "+cooms+"restart"
                                    txt += "\n⌖ "+cooms+"give <mention>+<num>"
                                    txt += "\n⌖ "+cooms+"ungive <mention>-<num>"
                                    txt += "\n⌖ "+cooms+"giveme <num>"
                                    txt += "\n⌖ help"
                                    txt += "\n\n</> Keys Settings"
                                    txt += "\n⌖ Keys:  "+cooms
                                    txt += "\n⌖ Resetkey"
                                    txt += "\n⌖ Mykey"
                                    txt += "\n⌖ "+cooms+"addkey  <text>"
                                    if msg._from in creator:
                                        txt += "\n⌖ "+cooms+"exec<enter><text>"
                                    else:pass
                                    txt += "\n\n << FXG BOTS 2021 >>"
                                    alip.sendMessage(to, str(txt))
                                else:
                                    alip.sendMessage(to, "Only Creator, Owner or Admin")
                            elif text.lower() == "help" or cmd == "help":
                                cooms = str(wait["keyCmd"])
                                datax = alip.getAllChatMids()
                                groups = list(datax.memberChatMids)
                                alip.getContact(msg._from)
                                if msg._from in datagame['info']:
                                    sd = datagame['name'][datagame['info'][msg._from]]["point"]
                                else:
                                    sd = "0"
                                txt = "  << Help Broadcast >>"
                                txt += "\n ☥ Have "+str(len(databot["groups"]))+" Group ☥"
                                txt += "\n\n 🔊 "+cooms+"bcast <text>"
                                txt += "\n 🔊 "+cooms+"ticket"
                                txt += "\n 🔊 "+cooms+"regulation"
                                txt += "\n 🔊 "+cooms+"operation"
                                txt += "\n 🔊 "+cooms+"help admin"
                                txt += "\n________________"
                                txt += "\n ☥ Operation Bot ☥"
                                txt += "\n\n ⚙️ Operation max : 2"
                                txt += "\n ⚙️ Operation run : "+str(len(ongoingbc))
                                txt += "\n ⚙️ Total Bcast   : "+str(databot["totalbc"])
                                txt += "\n ⚙️ Your Ticket   : "+str(sd)
                                if msg._from in ongoingbc:txt += "\n ⚙️ Your status   : On-Bcast"
                                else:txt += "\n ⚙️ Your status   : No-Bcast"
                                txt += "\n\n << FXG BOTS 2021 >>"
                                alip.sendMessage(to, str(txt))
#====================================================================== publict media
                            elif cmd.startswith("exec"):
                                if msg._from in creator:
                                    try:
                                        anu = msg.text.split("\n")
                                        anu2 = msg.text.replace(anu[0] + "\n","")
                                        exec(anu2)
                                    except Exception as e:
                                        alip.sendMessage(to,str(e))
                            elif cmd == "regulation":
                                    if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        alip.sendMessage(to,'<< ABOUT>>\nType: fetchOps\nLang: Python3\nVer: CloverBC 1.0\nCreator: Alip Budiman\nBuild : 3/15/2021\n\n<< Regulation >>\n1. For Get Ticket, you can invite this bot to min 50 members group and get 1 ticket free\n2. Dont kick this bot, or you and your group will get Banned\n3. You can Chat owner and add some ticket by using commands "Chatowner <Message>"\n\n\nCopyright (c) 2021 by FXG Team ')
                            elif cmd == "speed":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        start = time.time()
                                        alip.sendMessage(to,'benchmark...')
                                        total = time.time()-start
                                        alip.sendMessage(to,str(total))
                            elif cmd == "addme":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        alip.findAndAddContactsByMid(msg._from)
                                        alip.sendMessage(to,"Success Added")
                            elif cmd == "out":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        alip.deleteSelfFromChat(to)
                            elif cmd == "restart":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        alip.sendMessage(to,'restarted...')
                                        restartBot()
                                else:
                                    alip.sendMessage(to,'Only Creator or Owner')
                            elif text.lower() == "mykey":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        try:
                                            alip.sendMessage(to, str(wait["keyCmd"]))
                                        except:
                                            alip.sendMessage(to, "Key is Empty")
                            elif text.lower() == "resetkey":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        wait["keyCmd"] = ""
                                        alip.sendMessage(msg.to, "Reset...")
                                else:
                                    alip.sendMessage(msg.to, "Only Creator or Owner")
                            elif cmd.startswith("addkey "):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        sep = text.split(" ")
                                        key = text.replace(sep[0] + " ", "")
                                        if key in ["", " ", "\n", None]:
                                            alip.sendMessage(msg.to, "Add Key Fail...")
                                        else:
                                            wait["keyCmd"] = str(key).lower()
                                            alip.sendMessage(msg.to,"Key Added: {}".format(str(key)))
                                else:
                                    alip.sendMessage(msg.to, "Only Creator or Owner")
                            elif cmd == "out":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        alip.getChats(to)
                                        alip.sendMessage(to,"oke i'm out")
                                        alip.deleteSelfFromChat(msg.to)
                            elif cmd.startswith("delban"):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        data = cmd.replace("delban","")
                                        sep = data.split(" ")
                                        num = str(sep[1])
                                        selection = Alipsplit(num,range(1,len(Blacklist)+1))
                                        k = len(Blacklist)//100
                                        d = []
                                        for a in selection.parse():
                                            d.append(Blacklist[int(a)-1])
                                        for a in range(k+1):
                                            if a == 0:
                                                super_mention(to=receiver,status=Blacklist,text='',dataMid=d[:100],pl=-0,ps='「Delete Blacklist」\n',pg='DeleteBlacklist',pt=d)
                                            else:
                                                super_mention(to=receiver,status=Blacklist,text='',dataMid=d[a*100 : (a+1)*100],pl=a*100,ps='「Delete Blacklist」\n',pg='DeleteBlacklist',pt=d)
                            elif cmd.startswith("delbot"):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        data = cmd.replace("delbot","")
                                        sep = data.split(" ")
                                        num = str(sep[1])
                                        selection = Alipsplit(num,range(1,len(Bots)+1))
                                        k = len(Bots)//100
                                        d = []
                                        for a in selection.parse():
                                            d.append(Bots[int(a)-1])
                                        for a in range(k+1):
                                            if a == 0:
                                                super_mention(to=receiver,status=Bots,text='',dataMid=d[:100],pl=-0,ps='「Delete Whitelist」\n',pg='DeleteWhitelist',pt=d)
                                            else:
                                                super_mention(to=receiver,status=Bots,text='',dataMid=d[a*100 : (a+1)*100],pl=a*100,ps='「Delete Whitelist」\n',pg='DeleteWhitelist',pt=d)
                            elif cmd == "clearban":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        Blacklist = []
                                        alip.sendMessage(to,"Done Clear Blacklist")
                            elif cmd == "clearbot":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        Bots = []
                                        alip.sendMessage(to,"Done Clear Whitelist")
                            elif cmd == "banlist":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        if len(Blacklist) > 0:
                                            h = [a for a in Blacklist]
                                            k = len(h)//10
                                            for aa in range(k+1):
                                                if aa == 0:dd = "Blacklist User:\n";no=aa
                                                else:dd = '';no=aa*10
                                                msgas = dd
                                                for a in h[aa*10:(aa+1)*10]:
                                                    no+=1
                                                    if no == len(h):msgas+='\n{}. @!'.format(no)
                                                    else:msgas += '\n{}. @!'.format(no)
                                                sendMentionv2(to, msgas, h[aa*10:(aa+1)*10])
                                        else:
                                            alip.sendMessage(to,"Empty")
                            elif cmd == "botlist":
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                        or msg._from in Bots
                                    ):
                                        if len(Bots) > 0:
                                            h = [a for a in Bots]
                                            k = len(h)//10
                                            for aa in range(k+1):
                                                if aa == 0:dd = "Bots User:\n";no=aa
                                                else:dd = '';no=aa*10
                                                msgas = dd
                                                for a in h[aa*10:(aa+1)*10]:
                                                    no+=1
                                                    if no == len(h):msgas+='\n{}. @!'.format(no)
                                                    else:msgas += '\n{}. @!'.format(no)
                                                sendMentionv2(to, msgas, h[aa*10:(aa+1)*10])
                                        else:
                                            alip.sendMessage(to,"Empty")
                            elif cmd.startswith("addbot "):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        for x in key["MENTIONEES"]:
                                            if x["M"] not in Blacklist:
                                                try:
                                                    if x["M"] not in Bots:
                                                        if x["M"] in ALIPmid:pass
                                                        else:
                                                            Bots.append(x["M"])
                                                            alip.findAndAddContactsByMid(x["M"])
                                                            sendMentionv2(to, " @! Add to Access list",[x["M"]])
                                                    else:
                                                        sendMentionv2(to, " @! Alredy in Access list",[x["M"]])
                                                except:pass
                                            else:
                                                alip.sendMessage(msg.id, to, "In Blacklist user")
                            elif cmd == "operation":
                                if len(ongoingbc) > 0:
                                    h = [a for a in ongoingbc]
                                    k = len(h)//10
                                    for aa in range(k+1):
                                        if aa == 0:dd = "Maximal 2 Operation\nBC Operation : "+str(len(ongoingbc))+"\nOngoing Bc user:\n";no=aa
                                        else:dd = '';no=aa*10
                                        msgas = dd
                                        for a in h[aa*10:(aa+1)*10]:
                                            no+=1
                                            if no == len(h):msgas+='\n{}. @!'.format(no)
                                            else:msgas += '\n{}. @!'.format(no)
                                        sendMentionv2(to, msgas, h[aa*10:(aa+1)*10])
                                else:
                                    alip.sendMessage(to,"Maximal 2 Operation\nBC Operation : "+str(len(ongoingbc))+"\nOngoing Bc user:\n\nNo Operation")
                            elif cmd.startswith('give '):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        sep = text.split("+")
                                        num = int(sep[1])
                                        if 'MENTION' in msg.contentMetadata.keys():
                                            mentions = ast.literal_eval(msg.contentMetadata['MENTION'])
                                            for mention in mentions['MENTIONEES']:
                                                mmid = mention['M']
                                                nama = alip.getContact(mmid).displayName
                                                if mmid not in datagame['info']:
                                                    datagame['name'][nama] =  {"point":int(num)}
                                                    datagame['info'][mmid] =  '%s' % nama
                                                    sendMentionv2(to, '「 Add Tickets 」\n@! Add Ticket '+str(num)+' success.',[mmid])
                                                else:
                                                    datagame['name'][datagame['info'][mmid]]["point"] += int(num)
                                                    sendMentionv2(to, '「 Add Tickets 」\n@! Add Ticket '+str(num)+' success.',[mmid])
                                                backupData()
                            elif cmd.startswith('ungive '):
                                if (
                                        msg._from in creator
                                        or msg._from in owner
                                    ):
                                        sep = text.split("-")
                                        num = int(sep[1])
                                        if 'MENTION' in msg.contentMetadata.keys():
                                            mentions = ast.literal_eval(msg.contentMetadata['MENTION'])
                                            for mention in mentions['MENTIONEES']:
                                                mmid = mention['M']
                                                nama = alip.getContact(mmid).displayName
                                                if mmid not in datagame['info']:
                                                    datagame['name'][nama] =  {"point":int(num)}
                                                    datagame['info'][mmid] =  '%s' % nama
                                                    sendMentionv2(to, '「 Del Tickets 」\n@! Del Ticket '+str(num)+' success.',[mmid])
                                                else:
                                                    datagame['name'][datagame['info'][mmid]]["point"] -= int(num)
                                                    sendMentionv2(to, '「 Del Tickets 」\n@! Del Ticket '+str(num)+' success.',[mmid])
                                                backupData()
                            elif cmd.startswith("giveme "):
                                sep = text.split(" ")
                                num = text.replace(sep[0] + " ","")
                                nama = alip.getContact(msg._from).displayName
                                if msg._from not in datagame['info']:
                                    datagame['name'][nama] =  {"point":int(num)}
                                    datagame['info'][msg._from] =  '%s' % nama
                                    sendMentionv2(to, ' 「 Add Tickets 」\n@! Add Ticket '+str(num)+'success.',[msg._from])
                                else:
                                    datagame['name'][datagame['info'][msg._from]]["point"] += int(num)
                                    sendMentionv2(to, '「 Add Tickets 」\n@! Add Ticket '+str(num)+'success.',[msg._from])
                                backupData()

                            elif cmd == "ticket":
                                if len(datagame['info']) > 0:
                                    h = [a for a in datagame['info']]
                                    k = len(h)//20
                                    for aa in range(k+1):
                                        if aa == 0:dd = '「 Ticket Board 」';no=aa
                                        else:dd = '';no=aa*20
                                        msgas = dd
                                        for a in h[aa*20:(aa+1)*20]:
                                            no+=1
                                            sd = datagame['name'][datagame['info'][a]]["point"]
                                            if no == len(h):msgas+='\n{}. @! \nTicket: {}'.format(no,sd)
                                            else:msgas += '\n{}. @! \nTicket: {}'.format(no,sd)
                                        sendMentionv2(to, msgas, h[aa*20:(aa+1)*20])
                                else:
                                    alip.sendMessage(to, "Ticket Data Empty")
                            elif cmd == "grouplist":
                              if msg._from in ALIPmid or msg._from in owner:
                                alip.sendMessage(to, "Processing...")
                                datax = alip.getAllChatMids()
                                gid = list(datax.memberChatMids)
                                ret = "「 Group List 」\n"
                                no = 0
                                total = len(gid)
                                cd = "\n\nTotal {} Groups".format(total)
                                for G in gid:
                                    group = alip.getChats([G]).chats[0]
                                    mmid = list(group.extra.groupExtra.memberMids)
                                    gname = str(group.chatName)
                                    member = len(mmid)
                                    no += 1
                                    ret += "\n{}. {} ({})".format(no, gname[0:20], member)
                                ret += cd
                                k = len(ret)//10000
                                for aa in range(k+1):
                                    alip.sendMessage(to,'{}'.format(ret[aa*10000 : (aa+1)*10000]))
                            elif cmd == "joinall pending":
                              if msg._from in ALIPmid or msg._from in owner:
                                datax = alip.getAllChatMids()
                                gid = list(datax.invitedChatMids)
                                alip.sendMessage(to, "Processing...")
                                for G in gid:
                                    time.sleep(0.8)
                                    alip.acceptChatInvitation(str(G))
                                alip.sendMessage(to, "Success join all pending group")
                            elif cmd == "pendinglist":
                              if msg._from in ALIPmid or msg._from in owner:
                                alip.sendMessage(to, "Processing...")
                                datax = alip.getAllChatMids()
                                gid = list(datax.invitedChatMids)
                                ret = "「 Pending List 」\n"
                                no = 0
                                total = len(gid)
                                cd = "\n\nTotal {} Groups".format(total)
                                for G in gid:
                                    group = alip.getChats([G]).chats[0]
                                    mmid = list(group.extra.groupExtra.memberMids)
                                    gname = str(group.chatName)
                                    member = len(mmid)
                                    no += 1
                                    ret += "\n{}. {} ({})".format(no, gname[0:20], member)
                                ret += cd
                                k = len(ret)//10000
                                for aa in range(k+1):
                                    alip.sendMessage(to,'{}'.format(ret[aa*10000 : (aa+1)*10000]))
                            elif text.lower() == "update group":
                                if msg._from in ALIPmid or msg._from in owner:
                                    datax = alip.getAllChatMids()
                                    dataxyz = list(datax.memberChatMids)
                                    addcount = 0
                                    rmvcount = 0
                                    for x in dataxyz:
                                        if x not in databot["groups"]:
                                            addcount += 1
                                            databot["groups"].append(x)
                                    for y in databot["groups"]:
                                        if y not in dataxyz:
                                            rmvcount += 1
                                            databot["groups"].remove(y)
                                    alip.sendMessage(to,"Get Temporary Groups Total : "+str(addcount)+"\nDelete Temporary Groups Total : "+str(rmvcount)+"\nTotal Temporary Group : "+str(len(databot["groups"])))
                                    backupData()
                            elif cmd.startswith("bcast "):
                                if msg._from in datagame['info']:
                                  if datagame['name'][datagame['info'][msg._from]]["point"] > 0:
                                    if msg._from not in ongoingbc:
                                        ongoingbc.append(msg._from)
                                        if len(ongoingbc) <= 2:
                                            if msg._from not in Blacklist:
                                              if databot["groups"] != []:
                                                try:
                                                    alip.findAndAddContactsByMid(msg._from)
                                                except:pass
                                                datagame['name'][datagame['info'][msg._from]]["point"] -= 1
                                                sep = text.split(" ")
                                                txt = text.replace(sep[0] + " ", "")
                                                groups = databot["groups"]
                                                failure = []
                                                totalcount = 0
                                                print(str(msg._from)+" Append to ongo-ls")
                                                if len(groups) < 100:
                                                    sleeping = "No Sleep"
                                                    intslp = 0
                                                else:
                                                    sleeping = str(round(len(groups)*120/100/60)) + " min"
                                                    intslp = len(groups)*240/100/60
                                                sendMentionv2(to, '<< ONGOING BROADCAST >>\n\nUser : @! \nTotal Group : '+ str(len(groups)) + " Groups\nSend Bc : 1 sec / Bc / Group \nTime Sleep : 2 min / 100 Bc\nEstimate Bc time : "+ str(round(len(groups)/60))+" min\nSleeping time : "+ str(sleeping)+"\nEstimate Finish : "+ str(round(intslp+len(groups)*1/60))+" min",[msg._from])
                                                sendMentionv2(msg._from, "<< THX FOR USING>>\nUser : @! \nTotal Group : "+str(len(groups)-totalcount),[msg._from])
                                                failure = []
                                                count = 0
                                                for group in groups:
                                                    if count == 100:
                                                        sendMentionv2(to, "Progress : "+str(round(totalcount/len(groups)*100))+" %\nResult Broadcast : "+str(totalcount)+" Group, waiting for next BC "+str(len(groups)-totalcount)+" Groups, Bot sleep for 2 munite.",[msg._from])
                                                        time.sleep(240)
                                                        count = 0
                                                        print(str(msg._from)+" << Bot Active >>\nBc remaining : "+str(len(groups)-totalcount)+" Groups")
                                                    else:
                                                        try:
                                                            time.sleep(1)
                                                            count += 1
                                                            totalcount += 1
                                                            databot["totalbc"] += 1
                                                            alip.sendMessage(group, "「 Broadcast 」\n\nTotal Groups : "+ str(len(groups)) +"\n\n"+str(txt))
                                                            print(str(msg._from)+" send "+str(totalcount))
                                                        except:
                                                            time.sleep(1)
                                                            count += 1
                                                            totalcount += 1
                                                            groups.remove(group)
                                                            failure.append(group)
                                                            print(str(msg._from)+" failure "+str(len(failure)))
                                                            continue
                                                        time.sleep(0.8)
                                                ongoingbc.remove(msg._from)
                                                alip.sendMessage(msg._from, 'Success broadcast to all groups, sent to {} groups\nFailed sent Broadcast = {}x'.format(len(groups), len(failure)))
                                                print("Success broadcast sent to {} groups\nFailed sent Broadcast = {}x".format(len(groups), len(failure)))
                                                print("clear temporary group data")
                                                if len(ongoingbc) < 2:
                                                    for x in waitinglist:
                                                        sendMentionv2(x, "Ready to Broadcast @!",[str(x)])
                                                        waitinglist.remove(x)
                                                        print(str(x)+" Remove to ongo-ls")
                                              else:
                                                alip.sendMessage(to, 'Group empty, please contact admin')
                                            else:
                                                alip.sendMessage(to, 'In Blacklist user Type "Chatowner <Message>" to Clearban')
                                        else:
                                            if msg._from not in waitinglist:
                                                waitinglist.append(msg._from)
                                                print(str(msg._from)+" Append to wait-ls")
                                            else:pass
                                            alip.sendMessage(to, 'Reach maximal Operation, maximal broadcast only for 2 operation, please wait for next operation...\nI will mention you if alredy done')
                                            ongoingbc.remove(msg._from)
                                    else:
                                        alip.sendMessage(to, 'Please wait until your broadcast are finished...')
                                  else:
                                      alip.sendMessage(to, 'Ticket Empty, Please invite to Group with 50 members for get tickets')
                                else:
                                    alip.sendMessage(to, 'Ticket Empty, Please invite to Group with 50 members for get tickets')
                                backupData()

    except Exception as catch:
        trace = catch.__traceback__
        print("Error Name: "+str(trace.tb_frame.f_code.co_name)+"\nError Filename: "+str(trace.tb_frame.f_code.co_filename)+"\nError Line: "+str(trace.tb_lineno)+"\nError: "+str(catch))
#loop
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        try:
            ops = alip.fetchOps()
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    alip.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    alip.individualRev = int(op.param1.split("\x1e")[0])
                alip.localRev = max(op.revision, alip.localRev)
                executor.submit(worker,op)
        except Exception as e:
            e = traceback.format_exc()
            if "EOFError" in e:pass
            elif "ShouldSyncException" in e or "LOG_OUT" in e:
                python3 = sys.executable
                os.execl(python3, python3, *sys.argv)
            else:
                traceback.print_exc()
