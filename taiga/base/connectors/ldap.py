# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2015 Ensky Lin <enskylin@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC

from django.conf import settings
from . import exceptions as exc

def login (username: str, password: str) -> tuple:
	server = getattr(settings, "LDAP_SERVER", None)
	DN = getattr(settings, "LDAP_DN_FORMAT", None).format(username=username)
	try:
		s = Server(server)
		c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user=DN, password=password, authentication=AUTH_SIMPLE, check_names=True)
	except:
		raise exc.LDAPLoginError({"error_message": "LDAP account or password incorrect."})

	email = username + getattr(settings, "LDAP_BASE_EMAIL", None).format(username=username)
	full_name = username
	return (email, full_name)