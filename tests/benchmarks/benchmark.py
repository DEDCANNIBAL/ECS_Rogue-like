from timeit import timeit

from tests.benchmarks import test_esc as escpp

N = 20


def benchmark_create(module):
    world = module.make_world()
    return timeit('module.create(world)', number=N, globals=locals())


def benchmark_view(module):
    world = module.make_world()
    module.create(world)
    return timeit('module.view(world)', number=N * 2, globals=locals())


def benchmark_get(module):
    world = module.make_world()
    return timeit('module.get(world)', number=N * 2, globals=locals())


def benchmark(module):
    print('Base: %.3f' % benchmark_create(module))
    print('View: %.3f' % benchmark_view(module))
    print('Get: %.3f' % benchmark_get(module))


print('escpp:')
benchmark(escpp)
