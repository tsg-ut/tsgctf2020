#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include <iostream>
#include <vector>


using namespace std;

typedef long long int lli;
typedef struct {
    PyObject_HEAD
    vector<PyObject *> *v;
} StdVec;

typedef struct {
    PyObject_HEAD
    vector<PyObject*>::iterator current;
    vector<PyObject*>::iterator end;
} StdVecIter;

static PyObject *
iter_next(StdVecIter *self, PyObject *args) {
    if (self->current != self->end) {
        PyObject *obj = *self->current;
        self->current++;
        Py_INCREF(obj);
        return obj;
    } else {
        return NULL;
    }
}

static void
StdVecIter_dealloc(StdVecIter *self)
{
    PyObject_Del(self);
}

static PyTypeObject StdVecIterType= {
    PyVarObject_HEAD_INIT(NULL, 0)
    "stdvec.StdVecIter",                       /* tp_name */
    sizeof(StdVecIter),            /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)StdVecIter_dealloc,     /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "std vec iterator",                      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,              /* tp_iter */
    (iternextfunc)iter_next,        /* tp_iternext */
    0,                              /* tp_methods */
    0,                              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    0,            /* tp_alloc */
    0,                     /* tp_new */
};

static void
StdVec_dealloc(StdVec *self)
{
    /*for (auto itr = self->v->begin(); itr != self->v->end(); itr++) {
        Py_DECREF(*itr);
    }
    delete self->v;*/
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
StdVec_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    StdVec *self = (StdVec *)type->tp_alloc(type, 0);
    self->v = new vector<PyObject *>;
    if (self->v == NULL) {
        Py_DECREF(self);
        return NULL;
    }
    return (PyObject *)self;
}

static PyObject*
iter(StdVec *self, PyObject *args){
    vector<PyObject *>::iterator st = self->v->begin();
    vector<PyObject *>::iterator ed = self->v->end();
    StdVecIter *itr = PyObject_New(StdVecIter, &StdVecIterType);
    itr->current = st;
    itr->end = ed;
    return (PyObject *)itr;
}

static PyObject*
get_idx(StdVec *self, PyObject *args){
    int idx;
    if (!PyArg_ParseTuple(args, "i", &idx)) {
        Py_RETURN_NONE;
    }
    if (idx < 0 && self->v->size() + idx >= 0) {
        idx = self->v->size() + idx;
    }
    unsigned long long uidx = idx;
    if (uidx < self->v->size()) {
        PyObject *obj = (*self->v)[uidx];
        Py_INCREF(obj);
        return obj;
    } else {
        Py_RETURN_NONE;
    }
}

static PyObject*
set_idx(StdVec *self, PyObject *args){
    lli idx;
    PyObject *val;
    if (!PyArg_ParseTuple(args, "LO", &idx, &val)) {
        Py_RETURN_NONE;
    }
    if (idx < 0 && self->v->size() + idx >= 0) {
        idx = self->v->size() + idx;
    }
    unsigned long long uidx = idx;
    if (uidx < self->v->size()) {
        Py_INCREF(val);
        (*self->v)[uidx] = val;
    }
    Py_RETURN_NONE;
}

static PyObject*
append(StdVec *self, PyObject *args){
    PyObject *val;
    if (!PyArg_ParseTuple(args, "O", &val)) {
        Py_RETURN_NONE;
    }
    Py_INCREF(val);
    self->v->push_back(val);
    Py_RETURN_NONE;
}

static PyObject* length(StdVec *self, PyObject *args){
    unsigned long long size = self->v->size();
    return Py_BuildValue("K", size);
}

static PyMethodDef StdVecMethods[] = {
    {"append", (PyCFunction)append, METH_VARARGS, "stdvec: append"},
    {"size", (PyCFunction)length, METH_NOARGS, "stdvec: size"},
    {"get", (PyCFunction)get_idx, METH_VARARGS, "stdvec: get"},
    {"set", (PyCFunction)set_idx, METH_VARARGS, "stdvec: set"},
    {NULL}
};

static PyTypeObject StdVecType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "stdvec.StdVec",                       /* tp_name */
    sizeof(StdVec),            /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)StdVec_dealloc,     /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "std vec",                      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    (getiterfunc)iter,              /* tp_iter */
    0,                              /* tp_iternext */
    StdVecMethods,                  /* tp_methods */
    0,                              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    0,            /* tp_alloc */
    StdVec_new,                     /* tp_new */
};


static struct PyModuleDef stdvecmodule = {
    PyModuleDef_HEAD_INIT,
    "stdvec",
    NULL,
    -1,
};

PyMODINIT_FUNC PyInit_stdvec (void) {
    PyObject *m;
    if (PyType_Ready(&StdVecType) < 0)
        return NULL;
    m = PyModule_Create(&stdvecmodule);
    if (m == NULL)
        return NULL;
    Py_INCREF(&StdVecType);

    if (PyModule_AddObject(m, "StdVec", (PyObject *) &StdVecType) < 0) {
        Py_DECREF(&StdVecType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
