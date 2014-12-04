""" This file implements a Table class
    that is designed to be the basis of any format

Requirements
------------
* astropy:
    provides a samp access (astropy.vo.samp) for both python 2 and 3
    refactored version of sampy

    provides a replacement to pyfits

.. note::

    pyfits can still be used instead but astropy is now the default
"""
from __future__ import (absolute_import, division, print_function)

__version__ = '2.0'

import sys
import numpy as np
from numpy.lib import recfunctions
from copy import deepcopy

try:
    from astropy.io import fits as pyfits
except ImportError:
    import pyfits

# ================================================================
# Python 3 compatibility behavior
# ================================================================
# remap some python 2 built-ins on to py3k behavior or equivalent
# Most of them become generators
import operator

PY3 = sys.version_info[0] > 2

if PY3:
    iteritems = operator.methodcaller('items')
    itervalues = operator.methodcaller('values')
    basestring = (str, bytes)
else:
    range = xrange
    from itertools import izip as zip
    iteritems = operator.methodcaller('iteritems')
    itervalues = operator.methodcaller('itervalues')
    basestring = (str, unicode)


# ==========================================================================
# SimpleTable -- provides table manipulations with limited storage formats
# ==========================================================================
class SimpleTable(object):

    def __init__(self, fname, *args, **kwargs):

        dtype = kwargs.pop('dtype', None)
        self._aliases = {}
        self.caseless = kwargs.get('caseless', False)

        if (type(fname) == dict) or (dtype in [dict, 'dict']):
            self.header = fname.pop('header', {})
            self.data = self._convert_dict_to_structured_ndarray(fname)
        elif (type(fname) in (str,)) or (dtype is not None):
            if (type(fname) in (str,)):
                extension = fname.split('.')[-1]
            else:
                extension = None
            if (extension == 'csv') or dtype == 'csv':
                self.data = np.recfromcsv(fname, *args, **kwargs)
                self.header = {}
            elif (extension == 'tsv') or dtype == 'tsv':
                self.data = np.recfromtxt(fname, *args, **kwargs)
                self.header = {}
            elif (extension == 'fits') or dtype == 'fits':
                if ('extname' not in kwargs) and ('ext' not in kwargs) and (len(args) == 0):
                    args = (1, )
                self.data = np.array(pyfits.getdata(fname, *args, **kwargs))
                self.header = pyfits.getheader(fname, *args, **kwargs)
            else:
                raise Exception('Format {0:s} not handled'.format(extension))
        elif type(fname) == np.ndarray:
            self.data = fname
            self.header = {}
        elif type(fname) == pyfits.FITS_rec:
            self.data = np.array(fname)
            self.header = {}
        elif type(fname) == SimpleTable:
            cp = kwargs.pop('copy', True)
            if cp:
                self.data = deepcopy(fname.data)
                self.header = deepcopy(fname.header)
            else:
                self.data = fname.data
                self.header = fname.header
        else:
            raise Exception('Type {0!s:s} not handled'.format(type(fname)))
        if 'NAME' not in self.header:
            self.header['NAME'] = 'No Name'

    def write(self, fname, **kwargs):
        extension = fname.split('.')[-1]
        if (extension == 'csv'):
            np.savetxt(fname, self.data, delimiter=',', header=self.header, **kwargs)
        elif (extension in ['txt', 'dat']):
            np.savetxt(fname, self.data, delimiter=' ', header=self.header, **kwargs)
        elif (extension == 'fits'):
            append = kwargs.pop('append', False)
            if append:
                pyfits.append(fname, self.data,
                              pyfits.Header(self.header.items()), **kwargs)
            else:
                pyfits.writeto(fname, self.data,
                               pyfits.Header(self.header.items()), **kwargs)
        else:
            raise Exception('Format {0:s} not handled'.format(extension))

    def _convert_dict_to_structured_ndarray(self, data):
        """convert_dict_to_structured_ndarray

        Parameters
        ----------

        data: dictionary like object
            data structure which provides iteritems and itervalues

        returns
        -------
        tab: structured ndarray
            structured numpy array
        """
        newdtype = []
        for key, dk in iteritems(data):
            _dk = np.asarray(dk)
            dtype = _dk.dtype
            # unknown type is converted to text
            if dtype.type == np.object_:
                if len(data) == 0:
                    longest = 0
                else:
                    longest = len(max(_dk, key=len))
                    _dk = _dk.astype('|%iS' % longest)
            if _dk.ndim > 1:
                newdtype.append((str(key), _dk.dtype, (_dk.shape[1],)))
            else:
                newdtype.append((str(key), _dk.dtype))
        tab = np.rec.fromarrays(itervalues(data), dtype=newdtype)
        return tab

    def set_alias(self, alias, colname):
        """
        Define an alias to a column

        Parameters
        ----------
        alias: str
            The new alias of the column

        colname: str
            The column being aliased
        """
        if not (colname in self.keys()):
            raise KeyError("Column {0:s} does not exist".format(colname))
        self._aliases[alias] = colname

    def reverse_alias(self, colname):
        """
        Return aliases of a given column.

        Given a colname, return a sequence of aliases associated to this column
        Aliases are defined by using .define_alias()
        """
        _colname = self.resolve_alias(colname)
        if not (_colname in self.keys()):
            raise KeyError("Column {0:s} does not exist".format(colname))

        return tuple([ k for (k, v) in self._aliases.iteritems() if (v == _colname) ])

    def resolve_alias(self, colname):
        """
        Return the name of an aliased column.

        Given an alias, return the column name it aliases. This
        function is a no-op if the alias is a column name itself.

        Aliases are defined by using .define_alias()
        """
        # User aliases
        if hasattr(colname, '__iter__') & (type(colname) not in basestring):
            return [ self.resolve_alias(k) for k in colname ]
        else:
            if self.caseless is True:
                maps = dict( [ (k.lower(), v) for k, v in self._aliases.items() ] )
                maps.update( (k.lower(), k) for k in self.keys() )
                return maps.get(colname.lower(), colname)
            else:
                return self._aliases.get(colname, colname)

    def keys(self):
        return self.colnames

    @property
    def name(self):
        return self.header.get('NAME', None)

    @property
    def colnames(self):
        return self.data.dtype.names

    @property
    def ncols(self):
        return len(self.colnames)

    @property
    def nrows(self):
        return len(self.data)

    @property
    def nbytes(self):
        """ return the number of bytes of the object """
        n = sum(k.nbytes if hasattr(k, 'nbytes') else sys.getsizeof(k) for k in self.__dict__.values())
        return n

    def __len__(self):
        return self.nrows

    @property
    def shape(self):
        return self.data.shape

    @property
    def dtype(self):
        return self.data.dtype

    def __getitem__(self, v):
        return np.asarray(self.data.__getitem__(self.resolve_alias(v)))

    def __setitem__(self, k, v):
        if k in self:
            return self.data.__setitem__(self.resolve_alias(k), v)
        else:
            object.__setitem__(self, k, v)

    def __getattr__(self, k):
        try:
            return self.data.__getitem__(self.resolve_alias(k))
        except:
            return object.__getattribute__(self, k)

    def __iter__(self):
        return self.data.__iter__()

    def iterkeys(self):
        for k in self.keys():
            yield k

    def itervalues(self):
        for l in self.data:
            yield l

    def __repr__(self):
        s = object.__repr__(self)
        s += "\nTable: {name:s} nrows={s.nrows:d}, ncols={s.ncols:d}"
        return s.format(name=self.header.get('NAME', 'Noname'), s=self)

    def __getslice__(self, i, j):
        return self.data.__getslice__(i, j)

    def __contains__(self, k):
        return (k in self.keys()) or (k in self._aliases)

    def __array__(self):
        return self.data

    def sort(self, keys, copy=False):
        """
        Sort the table inplace according to one or more keys. This operates on
        the existing table (and does not return a new table).

        Parameters
        ----------

        keys: str or seq(str)
            The key(s) to order by

        copy: bool
            if set returns a sorted copy instead of working inplace
        """
        if not hasattr(keys, '__iter__'):
            keys = [keys]

        if copy is False:
            self.data.sort(order=keys)
        else:
            t = self.__class__(self, copy=True)
            t.sort(keys, copy=False)
            return t

    def match(self, r2, key):
        """ Returns the indices at which the tables match
        matching uses 2 columns that are compared in values

        Parameters
        ----------
        r2:  Table
            second table to use

        key: str
            fields used for comparison.

        Returns
        -------
        indexes: tuple
            tuple of both indices list where the two columns match.
        """
        return np.where( np.equal.outer( self[key], r2[key] ) )

    def stack(self, r, defaults=None):
        """
        Superposes arrays fields by fields inplace

        Parameters
        ----------
        r: Table
        """
        if not hasattr(r, 'data'):
            raise AttributeError('r should be a Table object')
        self.data = recfunctions.stack_arrays([self.data, r.data], defaults,
                                              usemask=False, asrecarray=True)

    def join_by(self, r2, key, jointype='inner', r1postfix='1', r2postfix='2',
                defaults=None, asrecarray=False, asTable=True):
        """
        Join arrays `r1` and `r2` on key `key`.

        The key should be either a string or a sequence of string corresponding
        to the fields used to join the array.
        An exception is raised if the `key` field cannot be found in the two input
        arrays.
        Neither `r1` nor `r2` should have any duplicates along `key`: the presence
        of duplicates will make the output quite unreliable. Note that duplicates
        are not looked for by the algorithm.

        Parameters
        ----------
        key: str or seq(str)
            corresponding to the fields used for comparison.

        r2: Table
            Table to join with

        jointype: str in {'inner', 'outer', 'leftouter'}
            * 'inner'     : returns the elements common to both r1 and r2.
            * 'outer'     : returns the common elements as well as the elements of r1 not in r2 and the elements of not in r2.
            * 'leftouter' : returns the common elements and the elements of r1 not in r2.

        r1postfix: str
            String appended to the names of the fields of r1 that are present in r2

        r2postfix:  str
            String appended to the names of the fields of r2 that are present in r1

        defaults:   dict
            Dictionary mapping field names to the corresponding default values.

        Returns
        -------
        tab: Table
            joined table

        .. note::

            * The output is sorted along the key.

            * A temporary array is formed by dropping the fields not in the key
              for the two arrays and concatenating the result. This array is
              then sorted, and the common entries selected. The output is
              constructed by filling the fields with the selected entries.
              Matching is not preserved if there are some duplicates...
        """
        arr = recfunctions.join_by(key, self, r2, jointype=jointype,
                                   r1postfix=r1postfix, r2postfix=r2postfix,
                                   defaults=defaults, usemask=False,
                                   asrecarray=True)

        return SimpleTable(arr)

    @property
    def empty_row(self):
        """ Return an empty row array respecting the table format """
        return np.rec.recarray(shape=(1,), dtype=self.data.dtype)

    def add_column(self, name, data, dtype=None, before=None, after=None, position=None):
        """
        Add a column to the table

        Parameters
        ----------
        name: str
           The name of the column to add

        data: ndarray
            The column data

        dtype: dtype
            numpy dtype for the data

        before: str
            Column before which the new column should be inserted

        after: str
            Column after which the new column should be inserted

        position:
            Position at which the new column should be inserted (0 = first)
        """

        _data = np.array(data, dtype=dtype)
        dtype = _data.dtype

        # unknown type is converted to text
        if dtype.type == np.object_:
            if len(data) == 0:
                longest = 0
            else:
                longest = len(max(data, key=len))
                data = np.asarray(data, dtype='|%iS' % longest)

        dtype = data.dtype

        if data.ndim > 1:
            newdtype = (str(name), data.dtype, (data.shape[1],))
        else:
            newdtype = (str(name), data.dtype)

        # get position
        if before:
            try:
                position = list(self.colnames).index(before)
            except:
                raise Exception("Column %s does not exist" % before)
        elif after:
            try:
                position = list(self.colnames).index(after) + 1
            except:
                raise Exception("Column %s does not exist" % before)

        if len(self.data.dtype) > 0:
            self.data = recfunctions.append_field(self.data, data, dtype=newdtype, position=position)
        else:
            self.data = np.array(data, dtype=[newdtype])

    def append_row(self, iterable):
        """
        Append one row in this table.

        see also: :func:`stack`

        Parameters
        ----------
        iterable: iterable
            line to add
        """
        assert( len(iterable) == self.ncols ), 'Expecting as many items as columns'
        r = self.empty_row
        for k, v in enumerate(iterable):
            r[0][k] = v
        self.stack(r)

    addLine = append_row

    def remove_columns(self, names):
        """
        Remove several columns from the table

        Parameters
        ----------
        names: sequence
            A list containing the names of the columns to remove
        """
        self.pop_columns(names)

    remove_column = delCol = remove_columns

    def pop_columns(self, names):
        """
        Pop several columns from the table

        Parameters
        ----------

        names: sequence
            A list containing the names of the columns to remove

        Returns
        -------

        values: tuple
            list of columns
        """

        if not hasattr(names, '__iter__') or type(names) in [str]:
            names = [names]

        p = [self[k] for k in names]

        _names = set([ self.resolve_alias(k) for k in names ])
        self.data = recfunctions.drop_fields(self.data, _names)
        for k in names:
            self._aliases.pop(k, None)

        return p

    def find_duplicate(self, index_only=False, values_only=False):
        """Find duplication in the table entries, return a list of duplicated
        elements Only works at this time is 2 lines are *the same entry* not if
        2 lines have *the same values*
        """
        dup = []
        idd = []
        for i in range(len(self.data)):
            if (self.data[i] in self.data[i + 1:]):
                if (self.data[i] not in dup):
                    dup.append(self.data[i])
                    idd.append(i)
        if index_only:
            return idd
        elif values_only:
            return dup
        else:
            return zip(idd, dup)

    def evalexpr(self, expr, exprvars=None, dtype=float):
        """ evaluate expression based on the data and external variables
            all np function can be used (log, exp, pi...)

        Parameters
        ----------
        expr: str
            expression to evaluate on the table
            includes mathematical operations and attribute names

        exprvars: dictionary, optional
            A dictionary that replaces the local operands in current frame.

        dtype: dtype definition
            dtype of the output array

        Returns
        -------
        out : NumPy array
            array of the result
        """
        _globals = {}
        for k in ( list(self.keys()) + list(self._aliases.keys()) ):
            if k in expr:
                _globals[k] = self[k]

        if exprvars is not None:
            assert(hasattr(exprvars, 'keys') & hasattr(exprvars, '__getitem__' )), "Expecting a dictionary-like as condvars"
            for k, v in ( exprvars.items() ):
                _globals[k] = v

        # evaluate expression, to obtain the final filter
        r    = np.empty( self.nrows, dtype=dtype)
        r[:] = eval(expr, _globals, np.__dict__)

        return r

    def where(self, condition, condvars=None, *args, **kwargs):
        """ Read table data fulfilling the given `condition`.
        Only the rows fulfilling the `condition` are included in the result.

        Parameters
        ----------
        condition: str
            expression to evaluate on the table
            includes mathematical operations and attribute names

        condvars: dictionary, optional
            A dictionary that replaces the local operands in current frame.

        Returns
        -------
        out: ndarray/ tuple of ndarrays
            result equivalent to numpy.where

        """
        ind = np.where(self.evalexpr(condition, condvars, dtype=bool ), *args, **kwargs)
        return ind

    def select(self, fields, indices=None, **kwargs):
        """
        Select only a few fields in the table
        """
        if fields.count(',') > 0:
            _fields = fields.split(',')
        elif fields.count(' ') > 0:
            _fields = fields.split()
        else:
            _fields = fields

        if _fields == '*':
            if indices is None:
                return self
            else:
                tab = self.__class__(self[indices])
                for k in self.__dict__.keys():
                    if k not in ('data', ):
                        setattr(tab, k, deepcopy(self.__dict__[k]))
                return tab
        else:
            d = {}
            for k in _fields:
                _k = self.resolve_alias(k)
                if indices is not None:
                    d[k] = self[_k][indices]
                else:
                    d[k] = self[_k]
            d['header'] = deepcopy(self.header)
            tab = self.__class__(d)
            for k in self.__dict__.keys():
                if k not in ('data', ):
                    setattr(tab, k, deepcopy(self.__dict__[k]))
            return tab

    def selectWhere(self, fields, condition, condvars=None, **kwargs):
        """ Read table data fulfilling the given `condition`.
            Only the rows fulfilling the `condition` are included in the result.

        Parameters
        ----------
        condition: str
            expression to evaluate on the table
            includes mathematical operations and attribute names

        condvars: dictionary, optional
            A dictionary that replaces the local operands in current frame.

        Returns
        -------
        """
        if condition in [True, 'True', None]:
            ind = None
        else:
            ind = self.where(condition, condvars, **kwargs)

        tab = self.select(fields, indices=ind)

        return tab
