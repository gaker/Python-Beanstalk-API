'''

2011 - Greg Aker.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

import requests

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree  as ET
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class BeanstalkRequest(object):
    def __init__(self, account_name, user, password):
        self.username = user
        self.password = password
        self.api_url = 'https://{0}.beanstalkapp.com/api/'.format(account_name)

    def get_current_user(self):
        url = '{0}users/current.xml'.format(self.api_url)
        return self._do_request(url)

    def user(self, user_id=None):
        ''' Get User Information

            http://api.beanstalkapp.com/user.html

            >>> b.BeanstalkRequest('my_account', 'username', 'password')
            >>> b.user() // returns all users on an account
            >>> b.user(user_id=123456) // returns info on single user
        '''
        if user_id is None:
            url = '{0}users.xml'.format(self.api_url)
        else:
            url = '{0}users/{1}.xml'.format(self.api_url, user_id)

        return self._do_request(url)

    def create_user(self, login, email, first_name, last_name, password):
        ''' Create a new user

        >>> b.BeanstalkRequest('my_account', 'username', 'password')
        >>> u = b.create_user(
        ...     login='greg',
        ...     email='greg@example.com',
        ...     first_name='greg',
        ...     last_name='aker',
        ...     password="foobarbaz"
        ... )
        >>>
        >>>
        print u.content
        <?xml version="1.0" encoding="UTF-8"?>
        <user>
          <account-id type="integer">73216</account-id>
          <admin type="boolean">false</admin>
          <created-at type="datetime">2011-09-15T22:01:37-05:00</created-at>
          <email>greg@example.com</email>
          <first-name>greg</first-name>
          <id type="integer">218958</id>
          <last-name>aker</last-name>
          <login>greg</login>
          <timezone nil="true"></timezone>
          <updated-at type="datetime">2011-09-15T22:01:37-05:00</updated-at>
          <owner type="boolean">false</owner>
        </user>
        '''
        url = '{0}users.xml'.format(self.api_url)

        root = ET.Element('user')

        child = ET.Element('login')
        child.text = login
        root.append(child)

        child = ET.Element('email')
        child.text = email
        root.append(child)

        child = ET.Element('first_name')
        child.text = first_name
        root.append(child)

        child = ET.Element('last_name')
        child.text = last_name
        root.append(child)

        child = ET.Element('password')
        child.text = password
        root.append(child)

        xml = ET.tostring(root, encoding='utf-8')

        return self._do_request(url, data=xml)

    def repository(self, repo_id=None):
        ''' Repository Actions

            http://api.beanstalkapp.com/repository.html

        '''
        if repo_id:
            url = '{0}repositories/{1}.xml'.format(
                self.api_url,
                repo_id
            )
        else:
            url = '{0}repositories.xml'.format(self.api_url)

        return self._do_request(url)

    def _do_request(self, url, data=None):
        if data is not None:
            return requests.post(
                url,
                data=data,
                auth=(self.username, self.password),
                headers={'Content-Type': 'application/xml'}
            )

        return requests.get(
            url,
            auth=(self.username, self.password),
            headers={'Content-Type': 'application/xml'}
        )
