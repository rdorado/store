import bpy
import time


def get_meshes_from_asset(file_location):
    bpy.ops.wm.open_mainfile(filepath=file_location)
    return bpy.data.meshes.keys()




'''
 *************************************
'''
def file_info(filename):
    print("--> 2")
    bpy.ops.wm.open_mainfile(filepath="/data/circle-button1.blend")
    collection = bpy.data.collections['Collection']
    
    with open("/data/output.txt", "w") as file_object:
        file_object.write(str(bpy.data.meshes.keys()))
        file_object.write(str(dir(bpy.data.meshes)))
    return "result"

def render():
    
    start = time.time()
    def evaltime():
        return str(time.time() - start)
    print("Start: "+evaltime())
    bpy.ops.wm.open_mainfile(filepath="/data/cube.blend")
    
    print("Read file: "+evaltime())
    
    # find absolute path for output
    #current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    #absolute_output_filename = os.path.join(current_directory, output_filename)

    # gets and sets the scene
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 1
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'

    # render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "/data/image.png" #"E:/project/blender/python/Sprite.png"
    print("Before rendering file: "+evaltime())
    print("Finished: "+evaltime())
    bpy.ops.render.render(write_still = 1)
    return "/data/image.png"