# Grid Visualizer

##### a light python library to create and visualize grids

## Features
-   stable and fast grid datatype
-   dynamic window size
-   customizable color schemes
-   easy to implement

## Example

```python

    from pygame import event, time
    from GridVisualizer import Visualizer, Grid
    
    if __name__ == "__main__":
        grid = Grid(25, 25)
        visualizer = Visualizer(grid, 500, 500, 1)
        clock = time.Clock()
        fps = 15
    
        while True:
            grid.setRndValues(0, 1)  # fill grid with random values
            visualizer.handle_events(event.get())  # let the visualizer handle events (quit, resizing)
            visualizer.update()  # show new grid
            clock.tick(fps)  # wait to match desired fps
```

![](media/random_example.gif)