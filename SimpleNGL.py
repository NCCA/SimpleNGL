#!/usr/bin/env python
from PyQt5.QtGui import QOpenGLWindow,QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from  PyQt5.QtCore import *
import sys
from pyngl import *
from OpenGL.GL import *

class MainWindow(QOpenGLWindow) :
  
  def __init__(self, parent=None):
    super(QOpenGLWindow, self).__init__(parent)
    self.m_cam=Camera()
    self.m_mouseGlobalTX=Mat4()
    self.m_width=1024
    self.m_height=720
    self.setTitle('pyNGL demo')
    

  def initializeGL(self) :
    self.makeCurrent()
    NGLInit.instance()
    glClearColor( 0.4, 0.4, 0.4, 1.0 ) 
    glEnable( GL_DEPTH_TEST )
    glEnable( GL_MULTISAMPLE )
    shader=ShaderLib.instance()
    #shader.loadShader('Phong','shaders/PhongVertex.glsl','shaders/PhongFragment.glsl')
    shaderProgram = 'Phong'
    vertexShader  = 'PhongVertex'
    fragShader    = 'PhongFragment'
    shader.createShaderProgram( shaderProgram );
    shader.attachShader( vertexShader, ShaderType.VERTEX );
    shader.attachShader( fragShader, ShaderType.FRAGMENT );
    shader.loadShaderSource( vertexShader, "shaders/PhongVertex.glsl" );
    shader.loadShaderSource( fragShader, "shaders/PhongFragment.glsl" );
    shader.compileShader( vertexShader );
    shader.compileShader( fragShader );
    shader.attachShaderToProgram( shaderProgram, vertexShader );
    shader.attachShaderToProgram( shaderProgram, fragShader );
    shader.linkProgramObject( shaderProgram );


    shader.use('Phong')
    m=Material(STDMAT.GOLD)
    m.loadToShader( "material" );
    self.m_cam.set(Vec3(1,1,1),Vec3.zero(),Vec3.up())
    self.m_cam.setShape( 45.0, 720.0 / 576.0, 0.05, 350.0 )
    shader.setUniform( "viewerPos", self.m_cam.getEye().toVec3() )
    iv = self.m_cam.getViewMatrix()
    iv.transpose()
    light=Light( Vec3( -2.0, 5.0, 2.0 ), Colour( 1.0, 1.0, 1.0, 1.0 ), Colour( 1.0, 1.0, 1.0, 1.0 ),LightModes.POINTLIGHT )
    light.setTransform( iv );
    light.loadToShader( 'light' )


  def loadMatricesToShader(self) :
    shader = ShaderLib.instance()

    normalMatrix=Mat3();
    M            = self.m_mouseGlobalTX;
    MV           = M * self.m_cam.getViewMatrix();
    MVP          = M * self.m_cam.getVPMatrix();
    #normalMatrix = Mat3(MV);
    normalMatrix.inverse();
    shader.setUniform( "MV", MV );
    shader.setUniform( "MVP", MVP );
    shader.setUniform( "normalMatrix", normalMatrix );
    shader.setUniform( "M", M );
    print normalMatrix
  
  def paintGL(self):
    glViewport( 0, 0, self.m_width, self.m_height )
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    shader=ShaderLib.instance()
    shader.use('Phong')
    #shader.use('nglColourShader')
    #shader.setUniform('Colour',1.0,0.0,0.0,1.0)
    prim = VAOPrimitives.instance()
    self.loadMatricesToShader()
    prim.draw( "teapot" )

  def resizeGL(self, w,h) :
    self.m_width=int(w* self.devicePixelRatio())
    self.m_height=int(h* self.devicePixelRatio())
    self.m_cam.setShape( 45.0, float( w ) / h, 0.05, 350.0 )

    print self.m_width,self.m_height


  def keyPressEvent(self, event) :
    key=event.key()
    if key==Qt.Key_Escape :
      exit()
    elif key==Qt.Key_W :
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    elif key==Qt.Key_S :
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    self.update()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  format=QSurfaceFormat()
  format.setSamples(4);
  format.setMajorVersion(4);
  format.setMinorVersion(1);
  format.setProfile(QSurfaceFormat.CoreProfile);
  # now set the depth buffer to 24 bits
  format.setDepthBufferSize(24);
  # set that as the default format for all windows
  QSurfaceFormat.setDefaultFormat(format);

  window = MainWindow()
  window.setFormat(format)
  window.resize(1024,720)
  window.show()
  sys.exit(app.exec_())