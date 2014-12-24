import functools
import logging

logger = logging.getLogger("revscores.util.dependencies")

class DependencyLoop(RuntimeError):
    pass

class Dependent:
    
    def __init__(self, name, process, depends_on=None):
        self.name = name
        self.process = process
        self.depends_on = depends_on if depends_on is not None else []
        functools.update_wrapper(self, process)
    
    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0}.".format(self))
        return self.process(*args, **kwargs)
    
    def __str__(self):
        return "<" + self.name + ">"
    
    def __repr__(self):
        return "{0}({1}, process={2}, dependencies={3})" \
               .format(self.__class__.__name__,
                       self.name,
                       self.process,
                       [str(d) for d in self.dependencies])
    

class depends:
    """
    Decorator for functions that adds a list of dependencies.  Functions
    decorated with this decorator can expect to be called with their
    dependencies solved as *args by the `solve()` function.
    
    :Example:
        >>> from revscores.util.dependencies import depends
        >>> @depends()
        ... def foo():
        ...     return 5
        ...
        >>> @depends(on=[foo])
        ... def bar(foo):
        ...     return "Bar value: {0}".format(foo)
        ...
        >>> bar
        <bar>
        >>> bar.dependencies
        [<foo>]
    
    :Parameters:
        on : `list`
            A sorted of dependencies that correspond to the *args of the
            function
    """
    def __init__(self, on=None):
        self.dependencies = on
    
    def __call__(self, process):
        return Dependent(process.__name__, process, self.dependencies)
    

def solve(dependent, cache=None, history=None):
    """
    Calculates a dependent's value by solving dependencies.
    
    :Parameters:
        dependent : `Dependent` | `function`
            A dependent function to solve for.
        cache : `dict`
            A memoized cache of previously solved dependencies.
        history : `set`
            Used to detect loops in dependencies.
    
    :Returns:
        The result of executing the dependent with all dependencies resolved
    """
    cache = cache or {}
    history = history or set()
    
    # Check if we've already got this dependency
    if dependent in cache:
        return cache[dependent]
    else:
        
        # Check if the dependency is callable.  If not, we're SOL
        if not callable(dependent):
            raise RuntimeError("Can't solve dependency " + repr(dependent) + \
                               ".  " + type(dependent).__name__ + \
                               " is not callable.")
                
        # Check if we're in a loop.
        elif dependent in history:
            raise DependencyLoop("Dependency loop detected at " + \
                                 repr(dependent))
        
        # All is good.  Time to generate a value
        else:
            
            # Add to history so we can detect any loops on the way down.
            history.add(dependent)
            
            # Check if we're a dependent with explicit dependencies
            if hasattr(dependent, "dependencies"):
                dependencies = dependent.dependencies
            else:
                # No dependencies?  OK.  Let's try that.
                dependencies = []
            
            # Generate args from dependencies
            args = [solve(dependency, cache, history=history)
                    for dependency in dependencies]
            
            
            # Generate value
            value = dependent(*args)
            
            #
            cache[dependent] = value
            return cache[dependent]
