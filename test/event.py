import unittest

from nodula import event

class SimpleEventTests(unittest.TestCase):
    def setUp(self):
        self.event = event.Event('event')
        self.living_cbs = []

    def tearDown(self):
        self.event = None
        self.living_cbs = None

    def test_canCallback(self):
        a = []
        def cb():
            a.append(True)
        self.event.register(cb)
        self.event.trigger()
        self.assertEqual(a, [True])

    def test_cbParams(self):
        a = []
        def cb(*args):
            a.append(args)
        self.event.register(cb)
        self.event.trigger(1, 2.0, 'three')
        self.assertEqual(a, [(1, 2.0, 'three')])

    def test_priority(self):
        a = []
        def cb_gen(obj):
            ret = lambda obj=obj: a.append(obj)
            self.living_cbs.append(ret)
            return ret
        self.event.register(cb_gen(1), event.PRI.EVENT_NORMAL)
        self.event.register(cb_gen(2.0), event.PRI.EVENT_VERY_HIGH)
        self.event.register(cb_gen('three'), event.PRI.PRE_DISPATCH)
        self.event.trigger()
        self.assertEqual(a, ['three', 2.0, 1])

    def test_double_trigger(self):
        a = []
        def cb():
            a.append(True)
        self.event.register(cb)
        self.event.trigger()
        self.event.trigger()
        self.assertEqual(a, [True, True])

    def test_double_register(self):
        a = []
        def cb():
            a.append(True)
        self.event.register(cb)
        self.event.register(cb, event.PRI.EVENT_HIGH)
        self.event.trigger()
        self.assertEqual(a, [True, True])

    def test_default_params(self):
        ev2 = event.Event('ev2', 1, 2.0, keywd = 'keywd')
        a = []
        def cb(*args, **kwargs):
            a.append((args, kwargs))
        ev2.register(cb)
        ev2.trigger('three', keywd2 = 'keywd2')
        self.assertEqual(a, [((1, 2.0, 'three'), {'keywd': 'keywd', 'keywd2': 'keywd2'})])

    def test_pre_dispatch(self):
        ev2 = event.Event('ev2', 1.0)
        dispatch = lambda *args, **kwargs: ev2.trigger(*args, **kwargs)
        self.event.register(dispatch, event.PRI.PRE_DISPATCH)
        a = []
        def cb(*args, **kwargs):
            a.append((args, kwargs))
        ev2.register(cb)
        self.event.trigger(2.0, 'three', keywd = 'keywd')
        self.assertEqual(a, [((1, 2.0, 'three'), {'keywd': 'keywd'})])

    def test_register_block(self):
        event.PRI.register_block('BLOCK')
        a = []
        def cb_gen(obj):
            ret = lambda obj=obj: a.append(obj)
            self.living_cbs.append(ret)
            return ret
        self.event.register(cb_gen(1), event.PRI.PRE_DISPATCH)
        self.event.register(cb_gen(2.0), event.PRI.EVENT_NORMAL)
        self.event.register(cb_gen('three'), event.PRI.BLOCK_NORMAL)
        self.event.trigger()
        self.assertEqual(a, [1, 2.0, 'three'])

if __name__ == '__main__':
    unittest.main()
