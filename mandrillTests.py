from mandrill import Mandrill
from mandrill import Error

def sendMessage():
    CO_NAME = 'Red Herring'

    try:
    	# Create a Mandril client with given key
    	M = Mandrill('ZSwFD0tp9Lc4iCDVTi-lvQ')

    	# Create the message to be sent
    	# https://mandrillapp.com/api/docs/messages.python.html#method-send
    	message = {
    		'from_email': 'noratarano@gmail.com',
    		'from_name': 'Nora Tarano',
    		'headers': {'Reply-To': 'noratarano@gmail.com'},
    		'subject': 'Red Herring Alert',
    		'tags': ['test'],
    		'text': 'Hi,\nWe are ' + CO_NAME + ' and our goal is to increase internet security awareness by warning individuals whose e-mails have been compromised. Unfortunately, your e-mail (*|EMAIL|*) was found on a publicly accessible file (link below), potentially with other sentisitive information. We urge you to change your password or take other precautions to ensure that your sensitive information remains private.\n\nThe following is a link to the publicly available file containing your information: [FILELINK].\n\nMore information regarding internet security can be found at [ADDR].\n\nNote that we only used your e-mail address to send you this message. We will never use it for any other purpose.\n\nThank you, and we hope we could help.\n\nSincerely,\nThe ' + CO_NAME + ' Team',
    		'to': [{'email': 'noratarano@hotmail.com'}] }

    except Error, e:
    	# Mandrill errors are thrown as exceptions
    	print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    	raise

def sentTemplate():
    try:
        M = Mandrill('-DUetSCLhDtp3EU4C3Ymsg')
        template_content = []
    	message = {
    		'from_email': 'dog@deltaFunction.co',
    		'from_name': 'Dog',
    		'headers': {'Reply-To': 'inbox@deltaFunction.co'},
    		'subject': 'Your e-mail has been found in a compromised account list',
    		'tags': ['dog'],
            'global_merge_vars': [{"name": "LISTURL", "content": "http://test.list.test" }],
            'merge_tags':[],
    		'to': [{'email': 'seangarita@gmail.com'}] }

        result = M.messages.send_template(
            template_name = 'a-type',
            template_content = template_content,
            message = message,
            async = True,
            ip_pool = 'Main Pool')

    except Error, e:
    	# Mandrill errors are thrown as exceptions
    	print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    	raise

sentTemplate()