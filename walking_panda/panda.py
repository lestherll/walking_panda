from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class WalkingPanda(ShowBase):
    """
    WalkingPanda is a class that displays a panda in its natural habitat.
    There are various command line arguments the user can pass to control
    the program.

    The command line arguments implemented currently can: stop the rotation
    of the camera, control the speed of the movement of the camera, move
    the camera to top view, scale the panda, and control whether the panda
    is displayed or not

    Parameters
    ----------
        param bool no_rotate
            enable/disable rotation (defaults to False)
        :param float rot_speed
            speed of rotation (defaults to 1.0)
        :param bool top_view
            camera top view orientation (defaults to False)
        :param float scale
            scale panda actor (defaults to 1.0)
        :param bool size
            actual size of the panda actor (defaults to 0.005)
        :param float no_panda
            show panda actor or not (defaults to False)

    Instance Attributes
    -------------------
        :attr bool loop_bg_sound
            loop background music (defaults to True)
        :attr float bg_sound_vol
            volume of the background music (defaults to 0.5)

    Instance Methods
    -------
        :method spinCameraTask -> Int
            Spin the camera around the origin
        :method setDefaultView -> None
             Set camera to the default view
        :method setTopView -> None
             Set camera to top view
        :method setPanda -> None
            Set scale and render panda

    """

    def __init__(self, no_rotate=False, rot_speed=1.0, top_view=False,
                 scale=1.0, size=0.005, no_panda=False):
        """Constructs a WalkingPanda object that inherits from ShowBase"""
        ShowBase.__init__(self)

        # make parameters attribute so it can be accessed by instances
        self.no_rotate = no_rotate
        self.top_view = top_view
        self.no_panda = no_panda
        self.scale = scale
        self.size = size
        self.actual_size = self.scale * self.size   # calculate actual size of the panda actor
        self.rot_speed = rot_speed

        self.loop_bg_sound = True
        self.bg_sound_vol = 0.5

        # MAIN SCENE
        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)   # scale scene
        self.scene.setPos(-8, 42, 0)    # set position of the scene

        # Set default view every time the program starts
        self.setDefaultView()

        # Check if --no-rotate param was passed
        if self.no_rotate is False:
            # Add the spinCameraTask procedure to the task manager.
            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Override default view and set to top view if --top-view was passed
        if self.top_view is True:
            self.setTopView()

        # Load the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})

        # check if --no-panda was passed
        if self.no_panda is False:
            self.setPanda()     # Render panda actor
            self.pandaActor.loop("walk")    # Loop walking animation.

        # play and loop sound
        self.backgroundMusic = self.loader.loadSfx("sound/Forest-ambience.mp3")
        self.backgroundMusic.setLoop(self.loop_bg_sound)
        self.backgroundMusic.play()
        self.backgroundMusic.setVolume(self.bg_sound_vol)

    def spinCameraTask(self, task):
        """Task for spinning the camera"""
        angleDegrees = task.time * 6.0 * self.rot_speed
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def setDefaultView(self):
        """Set camera orientation to default view"""
        # set position of camera without disabling mouse
        base.trackball.node().setPos(0, 20, -3)

    def setTopView(self):
        """Set camera orientation to top view"""
        base.trackball.node().setPos(0, 20, 0)
        base.trackball.node().setHpr(0, 90, 0)

    def setPanda(self):
        """Wrapper method to set the scale and render the panda actor"""
        # Scale panda using calculated size
        self.pandaActor.setScale(self.actual_size, self.actual_size, self.actual_size)
        self.pandaActor.reparentTo(self.render)
