import discord
from random import *
import pickle
import smtplib

servers_members = {}
dict_for_ee = {}
dict_for_ee_recipients = []
member_database = []
random_greeting = ['Hi', 'Hello', 'sup', 'wassup']
pickle_in = open('userdict.pickle', 'rb')
userdict = pickle.load(pickle_in)
pickle_in.close()

pickle_in_server = open('serverdict for encrypted channels.pickle', 'rb')
serverdict_for_encrypted_channels = pickle.load(pickle_in_server)
pickle_in_server.close()

pickle_in_server_decrypting = open('server_dict for decrypting channels.pickle', 'rb')
server_dict_for_decrypting = pickle.load(pickle_in_server_decrypting)
pickle_in_server_decrypting.close()
client = discord.Client()

alphabet = 'abcdefghijklmnopqrstuvwxyz .,!?%()~=+-_*&^$#@/QWERTYUIOPASDFGHJKLZXCVBNM1234567890<>\'"|:'
encryptedchannel = 0


def end_to_cipher(msg):
    global L
    L = []
    Q = []
    MESS = []
    print(msg)
    for i in range(len(msg)):
        x = randint(1, 87)
        L.append(x)
        p = msg[i]
        q = alphabet.index(p)
        v = (q + x) % 86
        Q.append(alphabet[v])
    MESS.append('[ee]')
    for i in range(len(Q)):
        MESS.append(Q[i])
    return ''.join(MESS)


def decipher(msg):
    M = list(msg[::2])
    key = list(alphabet.index(i) for i in msg[1::2])
    E = []
    for o in range(len(M)):
        op = alphabet.index(M[o])
        E.append(alphabet[(int(op) - int(key[o])) % 86])
    return ''.join(E)


def cipher(msg):
    L = []
    Q = []
    MESS = []
    print(msg)
    for i in range(len(msg)):
        x = randint(1, 87)
        L.append(x)
        p = msg[i]
        q = alphabet.index(p)
        v = (q + x) % 86
        Q.append(alphabet[v])
    P = [alphabet[i] for i in L]
    MESS.append('`')
    for i in range(len(P)):
        MESS.append(Q[i])
        MESS.append(P[i])
    MESS.append('`')
    return ''.join(MESS)


def cipher_mail(msg):
    L = []
    Q = []
    MESS = []
    for i in range(len(msg)):
        x = randint(1, 87)
        L.append(x)
        p = msg[i]
        q = alphabet.index(p)
        v = (q + x) % 86
        Q.append(alphabet[v])
    P = [alphabet[i] for i in L]
    for i in range(len(P)):
        MESS.append(Q[i])
        MESS.append(P[i])
    return ''.join(MESS)


@client.event  # event decorator/wrapper
async def on_ready():
    print(f"we have logged in as {client.user}")
    on_channel = client.get_channel(589081306931920899)
    await on_channel.send('Bot is online')
    Game = discord.Game('/help')
    await client.change_presence(status=discord.Status.online, activity=Game)


channelgreenicecream = 'bot-testing'




@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}:{message.author.name}:{message.content}")
    dmstring = str(message.channel)
    global encryptedchannel, stored_msg_send, user_who_typed_ee, servers_members, string_for_cipher_ee, msg_mail
    if 'Direct Message' not in dmstring:
        servers_members[message.guild.id] = message.guild.members
        for members in servers_members[message.guild.id]:
            if members not in member_database:
                member_database.append(members)
            if members in member_database:
                pass

    async for msg in message.channel.history(limit=2):
        if msg.content == '**Ok, what can I encrypt for you?,please type your text:**' and msg.author.name == 'One-time pad' and message.author.name != 'One-time pad':
            async with message.channel.typing():
                await message.channel.send('Here you go...')
                stored_msg_send = cipher(message.content)
                await message.channel.send(stored_msg_send)
                await message.channel.send('Do you want me to send this to your preferred channel?')
                break

    if '<@588016500003176456>' in message.content:
        async with message.channel.typing():
            await message.channel.send(choice(random_greeting) + ' ' + message.author.name + '!, can I encrypt something for you?')

    elif message.content.lower() == 'nope' or message.content.lower() == 'no' or message.content.lower() == 'nah':
        async for msg in message.channel.history(limit=2):
            if msg.content[-33:] == ' can I encrypt something for you?':
                async with message.channel.typing():
                    await message.channel.send('Ok, if you need me, type `/help` or mention me(`@One-time pad`), have a nice day!')
                    break
        async for msg in message.channel.history(limit=2):
            if msg.content == 'Do you want me to send this to your preferred channel?' and msg.author.name == 'One-time pad' and message.author.name != 'One-time pad':
                async with message.channel.typing():
                    await message.channel.send('Ok, if you need me, type `/help` or mention me(`@One-time pad`), have a nice day!')
                    break

    elif message.content.lower() == 'yes' or message.content.lower() == 'ye' or message.content.lower() == 'yup':
        async for msg in message.channel.history(limit=2):
            if msg.content[-33:] == ' can I encrypt something for you?':
                async with message.channel.typing():
                    await message.channel.send('**Ok, what can I encrypt for you?,please type your text:**')
        async for msg in message.channel.history(limit=2):
            if msg.content == 'Do you want me to send this to your preferred channel?' and msg.author.name == 'One-time pad' and message.author.name != 'One-time pad':
                async with message.channel.typing():
                    await message.channel.send('ok')
                    userchannel2 = client.get_channel(userdict[message.author.id])
                    await userchannel2.send((stored_msg_send) + ' **sent by ' + message.author.name+'**')

    elif message.content.startswith('/ci') and message.author.name != 'One-time pad':
        async with message.channel.typing():
            await message.channel.send('**ciphered:**')
            await message.channel.send(cipher(message.content[4:]))

    elif message.content.startswith('/de') and message.author.name != 'One-time pad' and message.content[:8] != '/de [ee]':
        async with message.channel.typing():
            await message.channel.send('**deciphered:**')
            await message.channel.send(decipher(message.content[4:]))

    elif message.content == '/help':
        helpforOTP = open('OTP help.txt').read()
        user_help_variable = client.get_user(message.author.id)

        if user_help_variable.dm_channel is not None:
            async with message.channel.typing():
                await message.author.dm_channel.send(helpforOTP)

        else:
            async with message.channel.typing():
                await user_help_variable.create_dm()
                await message.author.dm_channel.send(helpforOTP)
                await message.channel.send('**Sent you a DM containing a list of commands!**')

    if 'Direct Message' in dmstring and message.author.name != 'One-time pad' and message.content.startswith(
            '/send') and message.author.id in userdict:
        async with message.channel.typing():
            await message.channel.send('ok')
            userchannel = client.get_channel(userdict[message.author.id])
            await userchannel.send(cipher(message.content[6:]) + ' **sent by ' + message.author.name+'**')

    elif 'Direct Message' in dmstring and message.author.name != 'One-time pad' and message.content.startswith(
            '/send') and message.author.id not in userdict:
        async with message.channel.typing():
            await message.channel.send('**You haven\'t set a channel yet!**')

    elif message.content == '/set' and 'Direct Message' not in dmstring:
        async with message.channel.typing():
            await message.channel.send('**Your channel has been set to:**')
            await message.channel.send(str(message.channel) + ' in ' + str(message.guild))
        channelvariable = message.channel.id
        userdict[message.author.id] = channelvariable

    if message.content == '/off' and message.author.id == 370247469876903937:
        on_channel = client.get_channel(589081306931920899)
        await message.channel.send('Bye!')
        await on_channel.send('Bot is offline')
        print(userdict)
        print(serverdict_for_encrypted_channels)
        pickle_out = open('userdict.pickle', 'wb')
        pickle.dump(userdict, pickle_out)
        pickle_out.close()
        pickle_out_servers = open('serverdict for encrypted channels.pickle', 'wb')
        pickle.dump(serverdict_for_encrypted_channels, pickle_out_servers)
        pickle_out_servers.close()
        pickle_out_server_decrypting = open('server_dict for decrypting channels.pickle', 'wb')
        pickle.dump(server_dict_for_decrypting, pickle_out_server_decrypting)
        pickle_out_server_decrypting.close()
        await client.close()

    if message.content == '/set encrypted channel':
        encryptedchannel = message.channel.id
        if message.guild.id in serverdict_for_encrypted_channels and serverdict_for_encrypted_channels[
            message.guild.id] == encryptedchannel:
            async with message.channel.typing():
                await message.channel.send('**Already set to current channel!**')

        elif message.guild.id not in serverdict_for_encrypted_channels:
            async with message.channel.typing():
                serverdict_for_encrypted_channels[message.guild.id] = encryptedchannel
                await message.channel.send('Encrypted channel set to:\'' + str(message.channel))
                await message.channel.send('**Messages from here on will be encrypted**')

        elif message.guild.id in serverdict_for_encrypted_channels and serverdict_for_encrypted_channels[
            message.guild.id] != encryptedchannel:
            async with message.channel.typing():
                await message.channel.send('Encrypted channel has now been set to the current channel')
                serverdict_for_encrypted_channels[message.guild.id] = encryptedchannel

    if 'Direct Message' not in dmstring:
        if message.guild.id in serverdict_for_encrypted_channels and message.author.name != 'One-time pad' and \
                serverdict_for_encrypted_channels[message.guild.id] == message.channel.id:
            await message.channel.send(cipher(message.content) + ' (' + message.author.name + ')')
            await message.delete()

        if message.content == '/encrypt channel history' and message.author.name != 'One-time pad':
            await message.channel.send('ok')
            async with message.channel.typing():
                async for msg in message.channel.history():
                    if msg.author.name != 'One-time pad':
                        await message.channel.send(cipher(msg.content) + ' (' + msg.author.name + ')')
                        await msg.delete()

        if message.content == '/remove encryption':
            serverdict_for_encrypted_channels[message.guild.id] = 0
            await message.channel.send('**Encryption removed!**')

    if message.content.startswith('/ee'):
        async with message.channel.typing():
            await message.channel.send('**End to end encryption enabled.**')
            await message.channel.send('**Enter your message:**')
            user_who_typed_ee = client.get_user(message.author.id)

    async for msg in message.channel.history(limit=2):
        if msg.content == '**Enter your message:**' and msg.author.name == 'One-time pad' and message.author == user_who_typed_ee and message.content != '/ee':
            string_for_cipher_ee = end_to_cipher(message.content)
            dict_for_ee[string_for_cipher_ee] = message.content+'('+message.author.name+')'
            end_to_cipher(message.content)
            async with message.channel.typing():
                await message.channel.send('**Now, type in the name of the recipient with their tag(for example: Watuhhhmelon#3104) or mention them:**')

    message_history_for_ee_mention = await message.channel.history(limit=2).flatten()
    if message_history_for_ee_mention[1].content == '**Now, type in the name of the recipient with their tag(for example: Watuhhhmelon#3104) or mention them:**':
        if message_history_for_ee_mention[0].content[-5] == '#':
            print(member_database)
            name_discriminator = message_history_for_ee_mention[0].content.split('#')
            for member in member_database:
                if member.name == name_discriminator[0] and int(member.discriminator) == int(
                        name_discriminator[1]):
                    ee_user_variable = client.get_user(member.id)
                    if ee_user_variable.dm_channel is not None:
                        async with message.channel.typing():
                            await ee_user_variable.dm_channel.send('`' + string_for_cipher_ee + '`')
                            break
                    else:
                        async with message.channel.typing():
                            await ee_user_variable.create_dm()
                            await ee_user_variable.dm_channel.send('`' + string_for_cipher_ee + '`')
                            dict_for_ee_recipients.append(ee_user_variable.id)
                            await message.channel.send('Sent message to '+'**'+ee_user_variable.name+'**')
                            break

        if message_history_for_ee_mention[0].content[-5] != '#':
            name_discriminator = list(message_history_for_ee_mention[0].content)
            del name_discriminator[:2]
            del name_discriminator[-1]
            for member in member_database:
                if member.id == int(''.join(name_discriminator)):
                    ee_user_variable = client.get_user(member.id)
                    if ee_user_variable.dm_channel is not None:
                        async with message.channel.typing():
                            await ee_user_variable.dm_channel.send('`' + string_for_cipher_ee + '`')
                            await message.channel.send('Sent message to ' +'**' +ee_user_variable.name+'**')

                    else:
                        async with message.channel.typing():
                            await ee_user_variable.create_dm()
                            await ee_user_variable.dm_channel.send('`' + string_for_cipher_ee + '`')
                            dict_for_ee_recipients.append(ee_user_variable.id)
                            await message.channel.send('Sent message to '+'**'+ee_user_variable.name+'**')

    if message_history_for_ee_mention[1].content == '**Enter recipient\'s email address:**':
        recipient_email_address = message_history_for_ee_mention[0].content
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('onetimepadbot@gmail.com', 'Protart1')

            subject = 'Super Secret Message:'
            body = cipher_mail(str(msg_mail[6:]))

            msgw = f'Subject: {subject}\n\n{body}'

            smtp.sendmail('onetimepadbot@gmail.com', recipient_email_address, msgw)
            await message.channel.send('Email sent to '+'**' + recipient_email_address + '**')

    if message.content.startswith('/de [ee]'):
        if message.content[4:] not in dict_for_ee:
            async with message.channel.typing():
                await message.channel.send('`The key for this message has either been destroyed or doesn\'t exist`')
        async with message.channel.typing():
            await message.channel.send(dict_for_ee[message.content[4:]])
            del dict_for_ee[message.content[4:]]
            await message.channel.send('`The key has been destroyed`')
    if message.content.startswith('/mail'):
        msg_mail = message.content
        await message.channel.send('**Enter recipient\'s email address:**')

    if message.content.lower() == '/set decrypting channel':
        if server_dict_for_decrypting[message.guild.id] == message.channel.id:
            await message.channel.send('Decrypting channel already set to this channel')
        elif server_dict_for_decrypting[message.guild.id] != message.channel.id:
            server_dict_for_decrypting[message.guild.id] = message.channel.id
            await message.channel.send('Decrypting channel set to this channel')
    if server_dict_for_decrypting[message.guild.id] == message.channel.id and message.author.name != 'One-time pad':
        await message.channel.send('`'+decipher(message.content)+'`')
        await message.delete()

client.run("secret token")
