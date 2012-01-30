#!/usr/bin/env python

#C: THIS FILE IS PART OF THE CYLC FORECAST SUITE METASCHEDULER.
#C: Copyright (C) 2008-2012 Hilary Oliver, NIWA
#C:
#C: This program is free software: you can redistribute it and/or modify
#C: it under the terms of the GNU General Public License as published by
#C: the Free Software Foundation, either version 3 of the License, or
#C: (at your option) any later version.
#C:
#C: This program is distributed in the hope that it will be useful,
#C: but WITHOUT ANY WARRANTY; without even the implied warranty of
#C: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#C: GNU General Public License for more details.
#C:
#C: You should have received a copy of the GNU General Public License
#C: along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import re

""" 
CYCLE TIME: YYYYMMDDHH(mm)
"""

class CycleTimeError( Exception ):
    """
    Attributes:
        message - what the problem is. 
    """
    def __init__( self, msg ):
        self.msg = msg
    def __str__( self ):
        return repr(self.msg)

class InvalidCycleTimeError( CycleTimeError ):
    pass

class ct( object ):

    def __init__( self, str ):
        self.parse( str )

    def parse( self, str ):
        if len( str ) == 10:
            # YYYYMMDDHH - append minutes and seconds
            self.strvalue = str + '0000'
        elif len( str ) == 12:
            # YYYYMMDDHHmm - append seconds
            self.strvalue = str + '00'
        elif len( str ) == 14:
            # YYYYMMDDHHmmss
            self.strvalue = str
        else:
            raise InvalidCycleTimeError, 'ERROR: Cycle Times must be YYYYMMDDHH[mm[ss]] not: ' + str

        self.strvalue_Y2H = self.strvalue[0:10]

        self.year    = self.strvalue[ 0:4 ]
        self.month   = self.strvalue[ 4:6 ]
        self.day     = self.strvalue[ 6:8 ]
        self.hour    = self.strvalue[ 8:10]
        self.minute  = self.strvalue[10:12]
        self.seconds = self.strvalue[12:14]
        
        # convert to datetime as a validity check!
        try:
            self.dtvalue = datetime.datetime( int(self.year), int(self.month),
                int(self.day), int(self.hour), int(self.minute),
                int(self.seconds))
        except ValueError,x:
            # returns sensible messages: "minute must be in 0..59"
            raise InvalidCycleTimeError( x.__str__() + ': ' + self.get_formatted() )

    def get( self, Y2H=True ):
        if Y2H:
            # YYYYMMDDHH
            return self.strvalue_Y2H
        else:
            # YYYYMMDDHHmmss
            return self.strvalue

    def get_formatted( self ):
        # YYYY/MM/DD HH:mm:ss
        return self.year + '/' + self.month + '/' + self.day + ' ' + \
                self.hour + ':' + self.minute + ':' + self.seconds

    def get_datetime( self ):
        return self.dtvalue

    def _str_from_datetime( self, dt ): 
        return dt.strftime( "%Y%m%d%H%M%S" )

    def increment( self, weeks=0, days=0, hours=0, minutes=0, seconds=0,
            microseconds=0, milliseconds=0 ): 
        # Can't increment by years or months easily - they vary in length.
        newdt = self.dtvalue + \
                datetime.timedelta( int(days), int(seconds),
                        int(microseconds), int(milliseconds), 
                        int(minutes), int(hours), int(weeks) )
        self.parse( self._str_from_datetime( newdt ))

    def decrement( self, weeks=0, days=0, hours=0, minutes=0, seconds=0,
            microseconds=0, milliseconds=0 ): 
        # Can't decrement by years or months easily - they vary in length.
        newdt = self.dtvalue - \
                datetime.timedelta( int(days), int(seconds),
                        int(microseconds), int(milliseconds), 
                        int(minutes), int(hours), int(weeks) )
        self.parse( self._str_from_datetime( newdt ))

    def clone( self ):
        return ct( self.strvalue )

    def subtract( self, ct ):
        # subtract this ct from me, return a timedelta
        # (.days, .seconds, .microseconds)
         return self.dtvalue - ct.dtvalue

    def subtract_hrs( self, ct ):
        # subtract this ct from me, return hours
        delta = self.subtract(ct)
        return int( delta.days * 24 + delta.seconds / 3600 + delta.microseconds / ( 3600 * 1000000 ))


if __name__ == "__main__":
    foo = ct( '20110526184359' )
    print foo.get(), foo.get_formatted()
    try:
        bar = ct('2011053918' )
    except CycleTimeError, x:
        print x 


