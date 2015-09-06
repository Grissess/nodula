'''
nodula -- Project Nodula
event -- Event Dispatch

This module implements the observer pattern by way of Event objects.

A single Event object represents an event that can happen. It has two
important interface methods:
-Event.register(callback[, priority]): Registers a callback function
 to run when the given event is triggered, at the given priority.
-Event.trigger(*args, **kwargs): Call all the callbacks registered
 for this event, ordered by priority.

The signature of events (the parameters passed to their callbacks) are
generally agreed upon at their definition; the Event object simply
passes arguments to the callbacks as it receives them. Additional
arguments to prepend (for positional arguments) or merge (for keyword
arguments) may be passed to the constructor, which is helpful for
Events which are constructed as instance attributes, for example.

Callbacks are held weakly; as methods, for example, the reference to
.im_self is not enough (through the weak reference) to keep the
instance alive. When the instance is garbage-collected, its active
callbacks are automatically removed. This means that such instances
must be stored elsewhere to remain alive.
'''

import weakref

class PRI:
	PRE_DISPATCH = 0  # Absolute highest priority, before callback dispatch -- used to trigger other "meta-events"

	# In-block constants:
	VERY_HIGH = 0
	HIGH = 1
	NORMAL = 2
	LOW = 3
	VERY_LOW = 4
	BLOCK_SZ = 5

	# Priority blocks:
	EVENT = 1
	PREV = EVENT
	@classmethod
	def register_block(cls, name):
		setattr(cls, name, cls.PREV + cls.BLOCK_SZ)
		cls.PREV += cls.BLOCK_SZ
	
	# Some disgusting magic for "{BLOCK}_{LEVEL}"
	class __metaclass__(type):
		def __getattr__(cls, attr):
			if '_' in attr:
				block, _, lev = attr.partition('_')
				return getattr(cls, block) + getattr(cls, lev)


class Event(object):
	__slots__ = ('name', 'callbacks', 'args', 'kwargs')
	def __init__(self, name, *args, **kwargs):
		self.name = name
		self.args = args
		self.kwargs = kwargs
		self.callbacks = {}
	def register(self, callback, priority = PRI.EVENT_NORMAL):
		if priority not in self.callbacks:
			self.callbacks[priority] = weakref.WeakSet()
		self.callbacks[priority].add(callback)
	def unregister(self, callback, priority = None):
		if priority is None:
			for set in self.callbacks.itervalues():
				set.discard(callback)
		else:
			if priority in self.callbacks:
				self.callbacks[priority].discard(set)
	def trigger(self, *args, **kwargs):
		items = sorted(self.callbacks.items(), key = lambda pair: pair[0])
		for pri, set in items:
			for callback in set:
				kw = self.kwargs.copy()
				kw.update(kwargs)
				callback(*(self.args + args), **kw)
