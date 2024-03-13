class Block:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return self.name


class BlockWorld:
    def __init__(self, height=5, width=10):
        self.height = height
        self.width = width
        self.matrix = [[None for _ in range(width)] for _ in range(height)]
        self.LOG = []

    def print_world(self):
        for row in self.matrix:
            print(" ".join([str(block) if block else "-" for block in row]))
        print()

    def place_block(self, block):
        if 1 <= block.x <= self.width and 1 <= block.y <= self.height:
            if block.y == 1:
                self.matrix[self.height - block.y][block.x - 1] = block
                self.LOG.append(f"Блок {str(block)} размещен на координатах ({block.x}, {block.y})")
                self.print_world()
            elif self.matrix[self.height - block.y + 1][block.x - 1] is not None:
                self.matrix[self.height - block.y][block.x - 1] = block
                self.LOG.append(f"Блок {str(block)} размещен на координатах ({block.x}, {block.y})")
                self.print_world()
            else:
                self.LOG.append(f'Нельзя поставить блок {str(block)} в воздух')
        else:
            print(f"Нельзя поставить блок {str(block)} за пределы платформы")

    def find_free_column(self):
        for x in range(self.width):
            if self.matrix[self.height - 1][x] is None:
                return x + 1
        return None

    def clear_above(self, block):
        deleted_blocks = []
        for y in range(block.y + 1, self.height + 1):
            if self.matrix[self.height - y][block.x - 1] is not None:
                deleted_blocks.append(self.matrix[self.height - y][block.x - 1])
                self.matrix[self.height - y][block.x - 1] = None
        return deleted_blocks

    def clear_above_and_move(self, block):
        deleted_blocks = self.clear_above(block)
        deleted_blocks.reverse()
        free_column = self.find_free_column()
        self.LOG.append(f"Очищение поверхности блока {str(block)}")
        if free_column is not None:
            for i, deleted_block in enumerate(deleted_blocks):
                deleted_block.x = free_column
                deleted_block.y = i + 1
                self.matrix[self.height - deleted_block.y][deleted_block.x - 1] = deleted_block
                self.LOG.append(f"Блок {str(deleted_block)} перемещен в "
                                f"{free_column}ый столбец")
        else:
            self.LOG.append(f"Нет свободных столбцов!")

    def take(self, block):
        self.matrix[self.height - block.y][block.x - 1] = None
        self.LOG.append(f"Взят блок {str(block)} с координат ({block.x}, {block.y})")

    def move_to(self, block, new_coordinates):
        self.take(block)
        block.x, block.y = new_coordinates[0], new_coordinates[1]
        self.matrix[self.height - new_coordinates[1]][new_coordinates[0] - 1] = block
        self.LOG.append(f"Блок {str(block)} перемещен на координаты ({block.x}, {block.y})")

    def put_on(self, block1, block2):
        self.LOG.append(f"Поставить блок {str(block1)} на {str(block2)}")
        if self.matrix[self.height - block1.y - 1][block1.x - 1] is not None:
            self.clear_above_and_move(block1)
            self.print_world()
            # self.LOG.append(f"Block {str(block1)}: Надо очистить поверхность!")
        new_coordinates = [block2.x, block2.y + 1]
        if self.matrix[self.height - new_coordinates[1]][new_coordinates[0] - 1] is not None:
            self.clear_above_and_move(block2)
            self.print_world()
            # self.LOG.append(f"Block {str(block2)}: Надо очистить поверхность!")

        self.move_to(block1, new_coordinates)
        self.LOG.append(f"Блок {str(block1)} поставлен на {str(block2)}")
        self.print_world()


if __name__ == "__main__":
    block_A = Block("A", 10, 1)
    block_B = Block("B", 5, 1)
    block_C = Block('C', 10, 2)
    block_D = Block('D', 1, 1)

    # Создаем объект мира блоков
    world = BlockWorld()
    # Помещаем блоки в мир
    world.place_block(block_A)
    world.place_block(block_B)
    world.place_block(block_C)
    world.place_block(block_D)

    world.put_on(block_C, block_B)
    world.put_on(block_D, block_C)
    # world.put_on(block_C, block_A)
    # world.put_on(block_D, block_B)
    world.put_on(block_A, block_B)

    with open('log.txt', 'w') as f:
        for log in world.LOG:
            f.write(log + '\n')
        f.close()
