通过NX装配part文件提取装配结构树中所有part文件到指定目录并打包

由于公司一直用NX6.0，在最终交付图纸时需要清理文件夹中未使用的文件，所以写了这个脚本。

借助NX安装目录的ugpc.exe文件实现，对于高于NX8.5的版本可以直接用NX自带的GC工具箱中的零组件更名及导出功能实现

推荐使用批处理文件版本，python版只是自己用来练手，写得烂，而且python打包成exe后程序包很大有12M。

批处理版需要添加到右键菜单后才可以使用，安装方法：
直接运行<安装.bat>文件，如果无法找到NX安装目录，则需要手动复制所有文件到NX安装目录下UGII目录，然后运行<添加右键菜单.bat>



ugpc说明文档：
使用 ugpc 复制装配部件
要复制整个装配，请将其移动到另一个目录或将其存档至磁带上，您必须在顶级父装配部件和装配使用的每个组件部件上都执行此操作。
使用“Unigraphics 打印组件实用工具 (ugpc)”可简化这些任务。这是在操作系统中运行的独立程序。它接受装配部件的名称作为输入，并返回该装配所使用的组件部件的列表。可将 ugpc 并入各种装配文件管理脚本中以确保处理所有相关部件和顶层装配。
注意：版本控制规则不是通过 ugpc 来应用的。 

如何运行 ugpc
要调用 ugpc，则输入：
ugpc <filename>
其中 <filename> 是某个装配文件的名称（扩展名为 .prt）。

例如，输入：
ugpc/users/joe/car.prt

将返回：
/users/joe/car.prt /users/joe/chassis.prt /users/joe/axle.prt /users/adrian/wheel.prt /users/library/bolt.prt

注意，命令行上指定的顶层装配包括在输出中。

如果需要，可以在命令行上指定多个装配部件。例如：
ugpc engine.prt axle.prt

公共组件仅显示一次。
ugpc 实用工具接受以下可选开关：

-s	设置输出的格式以显示结构。后面可以紧跟一个数字，表示每层缩进的空格数（默认值为 4）。例如，上述输出会显示为： 
ugpc -s car.prt /users/joe/car.prt   /users/joe/   /users/joe/axle.prt   /users/adrian/wheel.prt   /users/library/bolt.prt
或
ugpc -s1 car.prt /users/joe/car.prt   /users/joe/chassis.prt   /users/joe/axle.prt   /users/adrian/wheel.prt   /users/library/bolt.prt

-n 表示输出应包括指定装配中包括的各个组件的数量。例如：
ugpc -n car.prt /users/joe/car.prt 1 /users/joe/chassis.prt 1 /users/joe/axle.prt 2 /users/adrian/wheel.prt 4 /users/library/bolt.prt 16
如果不使用以下任何开关，则 ugpc 先在从目录位置（也就是为父装配指定的目录）搜索组件部件文件。如果在该位置未找到任何文件，则 ugpc 在按照保存的位置（也就是，使用与父装配及其子装配一起保存的部件文件的路径名）搜索文件。

-a	ugpc 只在按照保存的位置查找组件 

-p	可为 ugpc 指定查找组件部件时的搜索目录。
例如：
ugpc -p /users/joe assy.prt -p /assy/3rd-level_assy.prt
可以使用任意数目的 -p 开关。系统按照给定的顺序进行搜索，直至找到一个存在的文件。如果找不到任何文件，系统将搜索存储在父部件文件中的路径。在装配的每层都会重复此过程。
不搜索指定搜索目录的子目录。
在使用 -p 选项时，可以指定环境变量及命令 . 或 ..，但不是命令 ~/。
ugpc 实用工具从已经打印好的组件中推断要搜索的目录。这意味着，如果在操作系统中还没有移动组件，那么在不使用 -p 选项的情况下应该始终获得完全列表。
 

出错消息
有关显示出错消息的更多疑难解答，请参阅日志文件 system_log。
一个常见出错消息：
Default schema directory is NULL（默认方案目录为空）
如果显示此消息，请检查环境变量 UGII_SCHEMA。
