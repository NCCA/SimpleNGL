#!/usr/bin/python
from PySide2.QtGui import QOpenGLWindow,QSurfaceFormat
from PySide2.QtWidgets import QApplication
from  PySide2.QtCore import *
import sys
from pyngl import *
from OpenGL.GL import *


class UBO() :
  def __init_(self) :
    self.MVP=Mat4(1.0)
    self.normalMatrix=Mat4(1.0)
    self.M=Mat4(1.0)
  def __len__(self) :
    return sys.getsizeof(self.MVP)*3
    

class MainWindow(QOpenGLWindow) :
  
  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)
    self.mouseGlobalTX=Mat4()
    self.width=int(1024)
    self.height=int(720)
    self.setTitle('PySide2-pyNGL demo')
    self.spinXFace = int(0)
    self.spinYFace = int(0)
    self.rotate = False
    self.translate = False
    self.origX = int(0)
    self.origY = int(0)
    self.origXPos = int(0)
    self.origYPos = int(0)
    self.INCREMENT=0.01
    self.ZOOM=0.1
    self.modelPos=Vec3()
    self.lightPos=Vec4()
    self.transformLight=True

  def initializeGL(self) :
    self.makeCurrent()
    NGLInit.initialize()
    glClearColor( 0.4, 0.4, 0.4, 1.0 ) 
    glEnable( GL_DEPTH_TEST )
    glEnable( GL_MULTISAMPLE )
    ShaderLib.loadShader('PBR','shaders/PBRVertexPython.glsl','shaders/PBRFragment.glsl',ErrorExit.OFF)
    ShaderLib.use('PBR')

    # We now create our view matrix for a static camera
    From=Vec3(0.0, 2.0, 2.0 ) 
    to  =Vec3( 0.0, 0.0, 0.0 ) 
    up  =Vec3( 0.0, 1.0, 0.0 ) 
    # now load to our new camera
    self.view=lookAt(From,to,up) 
    self.projection=perspective( 45.0, float( self.width  / self.height), 0.5, 20.0 )
    ShaderLib.setUniform( 'camPos', From ) 
    # now a light
    self.lightPos.set( 0.0, 2.0, 2.0 ,1.0) 
    # setup the default shader material and light properties
    # these are 'uniform' so will retain their values
    ShaderLib.setUniform('lightPosition',self.lightPos.toVec3()) 
    ShaderLib.setUniform('lightColor',400.0,400.0,400.0) 
    ShaderLib.setUniform('exposure',2.2) 
    ShaderLib.setUniform('albedo',0.950, 0.71, 0.29) 

    ShaderLib.setUniform('metallic',1.02) 
    ShaderLib.setUniform('roughness',0.38) 
    ShaderLib.setUniform('ao',0.2) 
    VAOPrimitives.createTrianglePlane('floor',20,20,1,1,Vec3.up()) 
    ShaderLib.printRegisteredUniforms('PBR')
    ShaderLib.use(nglCheckerShader) 
    ShaderLib.setUniform('lightDiffuse',1.0,1.0,1.0,1.0) 
    ShaderLib.setUniform('checkOn',1) 
    ShaderLib.setUniform('lightPos',self.lightPos.toVec3()) 
    ShaderLib.setUniform('colour1',0.9,0.9,0.9,1.0) 
    ShaderLib.setUniform('colour2',0.6,0.6,0.6,1.0) 
    ShaderLib.setUniform('checkSize',60.0) 
    ShaderLib.printRegisteredUniforms(nglCheckerShader)
   

  def loadMatricesToShader(self) :
    ShaderLib.use('PBR')

    # ubo=UBO()

    # ubo.M=self.view*self.mouseGlobalTX 
    # ubo.MVP=self.projection*ubo.M 
    # ubo.normalMatrix=ubo.M
    # ubo.normalMatrix.inverse().transpose()
    M=self.view*self.mouseGlobalTX
    MVP=self.projection*M
    normalMatrix=M
    normalMatrix.inverse().transpose() 
    ShaderLib.setUniform('M',M)
    ShaderLib.setUniform('MVP',MVP)
    ShaderLib.setUniform('normalMatrix',normalMatrix)
    #ShaderLib.setUniformBuffer('TransformUBO',len(ubo),ubo.MVP)
    if self.transformLight == True :
      ShaderLib.setUniform('lightPosition',(self.mouseGlobalTX*self.lightPos).toVec3())
    
  def paintGL(self):
    try :
      self.makeCurrent()
      glViewport( 0, 0, self.width, self.height )
      glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
      ShaderLib.use('PBR')
      rotX=Mat4() 
      rotY=Mat4() 
      rotX.rotateX( self.spinXFace ) 
      rotY.rotateY( self.spinYFace ) 
      self.mouseGlobalTX = rotY * rotX 
      self.mouseGlobalTX.m_30  = self.modelPos.m_x 
      self.mouseGlobalTX.m_31  = self.modelPos.m_y 
      self.mouseGlobalTX.m_32  = self.modelPos.m_z 
      self.loadMatricesToShader()
      VAOPrimitives.draw('teapot')
      
      ShaderLib.use(nglCheckerShader)
      tx=Mat4()
      tx.translate(0.0,-0.45,0.0)
      MVP=self.projection*self.view*self.mouseGlobalTX*tx
      normalMatrix=Mat3(self.view*self.mouseGlobalTX)
      normalMatrix.inverse().transpose()
      ShaderLib.setUniform('MVP',MVP)
      ShaderLib.setUniform('normalMatrix',normalMatrix)
      VAOPrimitives.draw('floor')

    except OpenGL.error.GLError :
      print 'error'

  def resizeGL(self, w,h) :
    self.width=int(w* self.devicePixelRatio())
    self.height=int(h* self.devicePixelRatio())
    self.projection=perspective( 45.0, float( self.width)  / self.height, 0.5, 20.0 )


  def keyPressEvent(self, event) :
    key=event.key()
    if key==Qt.Key_Escape :
      exit()
    elif key==Qt.Key_W :
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    elif key==Qt.Key_S :
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    elif key==Qt.Key_Space :
      self.spinXFace=0
      self.spinYFace=0
      self.modelPos.set(Vec3.zero())
    elif key==Qt.Key_L :
      self.transformLight^=True
    
    self.update()

  def mouseMoveEvent(self, event) :
    if self.rotate and event.buttons() == Qt.LeftButton  :
      diffx = int(event.x() - self.origX)
      diffy = int(event.y() - self.origY)
      self.spinXFace += int( 0.5 * diffy )
      self.spinYFace += int( 0.5 * diffx )
      self.origX = event.x()
      self.origY = event.y()
      self.update()

    elif  self.translate and event.buttons() == Qt.RightButton :

      diffX   = int( event.x() - self.origXPos )
      diffY   = int( event.y() - self.origYPos )
      self.origXPos = event.x()
      self.origYPos = event.y()
      self.modelPos.m_x += self.INCREMENT * diffX 
      self.modelPos.m_y -= self.INCREMENT * diffY 
      self.update() 

  def mousePressEvent(self,event) :
    if  event.button() == Qt.LeftButton :
      self.origX  = event.x()
      self.origY  = event.y()
      self.rotate = True

    elif  event.button() == Qt.RightButton :
      self.origXPos  = event.x() 
      self.origYPos  = event.y() 
      self.translate = True

  def mouseReleaseEvent(self,event) :
    if  event.button() == Qt.LeftButton :
      self.rotate = False

    elif  event.button() == Qt.RightButton :
      self.translate = False

  def wheelEvent(self,event) :
    numPixels = event.pixelDelta() 

    if  numPixels.x() > 0  :
      self.modelPos.m_z += self.ZOOM

    elif  numPixels.x() < 0 :
      self.modelPos.m_z -= self.ZOOM
    self.update() 


if __name__ == '__main__':
  app = QApplication(sys.argv)
  format=QSurfaceFormat()
  format.setSamples(4) 
  format.setMajorVersion(4) 
  format.setMinorVersion(1) 
  format.setProfile(QSurfaceFormat.CoreProfile) 
  # now set the depth buffer to 24 bits
  format.setDepthBufferSize(24) 
  # set that as the default format for all windows
  QSurfaceFormat.setDefaultFormat(format) 

  window = MainWindow()
  window.setFormat(format)
  window.resize(1024,720)
  window.show()
  sys.exit(app.exec_())
