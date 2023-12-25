docker exec -it app /bin/sh

bar.apply_async((3, 1, 0), priority=10)
bar.apply_async((3, 2, 0), priority=10)
bar.apply_async((3, 3, 0), priority=10)
bar.apply_async((3, 4, 0), priority=10)
foo.apply_async((3, 1, 0), priority=0)
foo.apply_async((3, 2, 0), priority=0)
foo.apply_async((3, 3, 0), priority=0)
foo.apply_async((3, 4, 0), priority=0)
foo.apply_async((3, 5, 0), priority=0)
