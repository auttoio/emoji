#!/usr/bin/env python
import mechanize
import os, sys, getopt, re

def main(argv):
    team = ''
    email = ''
    password = ''
    url = ''
    try:
        opts, args = getopt.getopt(argv,"ht:e:p:",["team=","email=","password="])
    except getopt.GetoptError:
        print 'Error: Bad args'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python slack.py -t <team>'
            sys.exit()
        elif opt in ("-t", "--team"):
            team = arg
            url = 'https://' + team + '.slack.com/customize'
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
    if not (team and email and password):
        print "You must pass a team, email, and password."
    else:
        # Print the vars we set from args
        print "Team is {team!s}".format(**locals())
        print "Email is {email!s}".format(**locals())
        print "Password is {password!s}".format(**locals())
        print "URL is {url!s}".format(**locals())

        # Open a browser and login to a Slack team
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_redirect(True)
        br.open(url)
        br.select_form(nr=0)
        br.form['email'] = email
        br.form['password'] = password
        br.submit()

        # Upload emoji
        for fn in os.listdir('./emoji'):
            for form in br.forms():
                if form.attrs['id'] == 'addemoji':
                    br.form = form
                    break
            
	    prohibited = ['.png', '.jpg', '.gif']
	    replacement_regex = re.compile('|'.join(map(re.escape, prohibited)))
	    clean_name = replacement_regex.sub('', fn).replace('_', '-')
            br.form['name'] = clean_name

	    full_path = './emoji/' + fn

            br.form.add_file(open(full_path), 'image/*', full_path)
            br.submit()
            print 'Uploaded ', fn

if __name__ == "__main__":
    main(sys.argv[1:])
