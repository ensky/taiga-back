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

import pytest

from unittest.mock import patch, Mock
from taiga.base.connectors import ldap
from taiga.base.connectors import exceptions as exc

def test_ldap_login_success():
    BASE_EMAIL = "@example.com"
    with patch("taiga.base.connectors.ldap.Server") as m_server, \
            patch("taiga.base.connectors.ldap.Connection") as m_connection, \
            patch("taiga.base.connectors.ldap.BASE_EMAIL", new=BASE_EMAIL):
        m_server.return_value = Mock()
        m_connection.return_value = Mock()

        username = "**userName**"
        password = "**password**"
        (email, full_name) = ldap.login(username, password)
        assert email == username + BASE_EMAIL
        assert full_name == username


def test_ldap_login_fail():
    with pytest.raises(exc.LDAPLoginError) as e:
        username = "**userName**"
        password = "**password**"
        auth_info = ldap.login(username, password)

    assert e.value.status_code == 400
    assert "error_message" in e.value.detail