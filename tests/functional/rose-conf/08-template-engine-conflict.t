#!/usr/bin/env bash
# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
# Check that error raised when shebang != [template_engine:suite.rc] section.
. "$(dirname "$0")/test_header"
#-------------------------------------------------------------------------------
python -c "import cylc.rose" > /dev/null 2>&1 ||
  skip_all "cylc.rose not installed in environment."

set_test_number 2

install_suite "${TEST_NAME_BASE}" "${TEST_NAME_BASE}"

run_fail "${TEST_NAME_BASE}-validate" cylc validate "${SUITE_NAME}"

cmp_ok "${TEST_NAME_BASE}-validate.stderr" <<__HEREDOC__
FileParseError: Plugins set templating engine = empy which does not match #!jinja2 set in flow.cylc.
__HEREDOC__

purge
exit
