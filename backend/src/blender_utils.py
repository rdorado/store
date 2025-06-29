import bpy
import time

def render(blender_file, result_name):
    
    start = time.time()
    def evaltime():
        return str(time.time() - start)
    print("Start: "+evaltime())
    bpy.ops.wm.open_mainfile(filepath=blender_file)
    
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
    scene.render.filepath = result_name
    print("Before rendering file: "+evaltime())
    print("Finished: "+evaltime())
    bpy.ops.render.render(write_still = 1)