//
//  ViewController.swift
//  rotation
//
//  Created by Ethan Hardacre on 11/4/17.
//  Copyright © 2017 Ethan Hardacre. All rights reserved.
//

import UIKit
import CoreMotion
import SwiftSocket

class ViewController: UIViewController {
    
    let addr = "172.20.10.3"
    var client = UDPClient(address: "", port: 0)
    var previousOrientation = UIInterfaceOrientationMask()
    var swipe = UISwipeGestureRecognizer()
    var imgView = UIImageView()
    
    let manager = CMMotionManager()
    let range = 10.0
    let moveRangeV = 6
    let moveRangeH = 5
    var moto = 0.0
    var dir = 0
    var move = 0.0
    var waiting = false
    var movView = UIView()
    var currentPiece = ""
    var player1 = false
    var MAIN_HEIGHT:CGFloat = 0
    var MAIN_WIDTH: CGFloat = 0
    
    var player1Button = UIButton()
    var player2Button = UIButton()
    
    var generator = UIImpactFeedbackGenerator()

    override func viewDidLoad() {
        super.viewDidLoad()
        client = UDPClient(address: addr, port: 6969)
        
        generator = UIImpactFeedbackGenerator(style: .heavy)
        
        player1Button = UIButton(frame: CGRect(x: 10, y: view.frame.height/2 - 60, width: view.frame.width - 20, height: 50))
        player2Button = UIButton(frame: CGRect(x: 10, y: view.frame.height/2 + 10, width: view.frame.width - 20, height: 50))
        
        player1Button.backgroundColor = #colorLiteral(red: 0.1411764771, green: 0.3960784376, blue: 0.5647059083, alpha: 1)
        player1Button.layer.cornerRadius = 10
        player2Button.backgroundColor = #colorLiteral(red: 0.1411764771, green: 0.3960784376, blue: 0.5647059083, alpha: 1)
        player2Button.layer.cornerRadius = 10
        player1Button.addTarget(self, action: #selector(connectPlayer1), for: .touchUpInside)
        player2Button.addTarget(self, action: #selector(connectPlayer2), for: .touchUpInside)
        
        let text1 = UILabel(frame: CGRect(x: 0, y: 0, width: view.frame.width - 20, height: 50))
        text1.backgroundColor = UIColor.clear
        text1.textAlignment = .center
        text1.text = "Player 1"
        text1.textColor = #colorLiteral(red: 1, green: 1, blue: 1, alpha: 1)
        player1Button.addSubview(text1)
        
        let text2 = UILabel(frame: CGRect(x: 0, y: 0, width: view.frame.width - 20, height: 50))
        text2.backgroundColor = UIColor.clear
        text2.textAlignment = .center
        text2.text = "Player 2"
        text2.textColor = #colorLiteral(red: 1, green: 1, blue: 1, alpha: 1)
        player2Button.addSubview(text2)
    
        imgView = UIImageView(frame: CGRect(x: view.frame.width/2 - 250, y: view.frame.height/2 - 250, width: 500, height: 500))
        imgView.contentMode = .scaleAspectFit
        imgView.image = #imageLiteral(resourceName: "Tertis-1")
        
        view.addSubview(player1Button)
        view.addSubview(player2Button)

        view.backgroundColor = #colorLiteral(red: 0, green: 0, blue: 0, alpha: 1)
        self.view.addSubview(movView)
        manager.gyroUpdateInterval = 0.1
        swipe.direction = UISwipeGestureRecognizerDirection.down
        swipe.addTarget(self, action: #selector(drop))
        self.view.addGestureRecognizer(swipe)
        gyro_up()
        
        MAIN_HEIGHT = view.frame.height
        MAIN_WIDTH = view.frame.width

    }
    
    func connectPlayer1(){
        _ = client.send(string: "1")
        player1Button.removeFromSuperview()
        player2Button.removeFromSuperview()
        player1 = true
        self.view.addSubview(imgView)
        generator.prepare()
        generator.impactOccurred()
    }
    
    func connectPlayer2(){
        _ = client.send(string: "2")
        player1Button.removeFromSuperview()
        player2Button.removeFromSuperview()
        self.view.addSubview(imgView)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func drop(){
        generator.impactOccurred()
        if player1 {
            _ = self.client.send(string: "w")
        }else{
            _ = self.client.send(string: "i")
        }
    }
    
    override func willRotate(to toInterfaceOrientation: UIInterfaceOrientation, duration: TimeInterval) {
        generator.impactOccurred()
        switch toInterfaceOrientation {
        case UIInterfaceOrientation.portraitUpsideDown:
            if previousOrientation == UIInterfaceOrientationMask.landscapeLeft && player1{
                _ = self.client.send(string: "e")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeRight && player1{
                _ = self.client.send(string: "q")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeLeft && !player1{
                _ = self.client.send(string: "o")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeRight && !player1{
                _ = self.client.send(string: "u")
            }
            imgView.frame = CGRect(x: MAIN_WIDTH/2 - 250, y: MAIN_HEIGHT/2 - 250, width: 500, height: 500)
            previousOrientation = UIInterfaceOrientationMask.portraitUpsideDown
            gyro_down()
        case UIInterfaceOrientation.portrait:
            if previousOrientation == UIInterfaceOrientationMask.landscapeLeft && player1{
                _ = self.client.send(string: "q")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeRight && player1{
                _ = self.client.send(string: "e")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeLeft && !player1{
                _ = self.client.send(string: "u")
            }else if previousOrientation == UIInterfaceOrientationMask.landscapeRight && !player1{
                _ = self.client.send(string: "o")
            }
            imgView.frame = CGRect(x: MAIN_WIDTH/2 - 250, y: MAIN_HEIGHT/2 - 250, width: 500, height: 500)
            previousOrientation = UIInterfaceOrientationMask.portrait
            gyro_up()
        case UIInterfaceOrientation.landscapeLeft:
            if previousOrientation == UIInterfaceOrientationMask.portrait && player1{
                _ = self.client.send(string: "e")
            }else if previousOrientation == UIInterfaceOrientationMask.portraitUpsideDown && player1{
                _ = self.client.send(string: "q")
            }else if previousOrientation == UIInterfaceOrientationMask.portrait && !player1{
                _ = self.client.send(string: "o")
            }else if previousOrientation == UIInterfaceOrientationMask.portraitUpsideDown && !player1{
                _ = self.client.send(string: "u")
            }
            imgView.frame = CGRect(x: view.frame.height/2 - 250, y: view.frame.width/2 - 250, width: 500, height: 500)
            previousOrientation = UIInterfaceOrientationMask.landscapeLeft
            gyro_right()
        case UIInterfaceOrientation.landscapeRight:
            if previousOrientation == UIInterfaceOrientationMask.portrait && player1{
                _ = self.client.send(string: "q")
            }else if previousOrientation == UIInterfaceOrientationMask.portraitUpsideDown && player1{
                _ = self.client.send(string: "e")
            }else if previousOrientation == UIInterfaceOrientationMask.portrait && !player1{
                _ = self.client.send(string: "u")
            }else if previousOrientation == UIInterfaceOrientationMask.portraitUpsideDown && !player1{
                _ = self.client.send(string: "o")
            }
            imgView.frame = CGRect(x: view.frame.height/2 - 250, y: view.frame.width/2 - 250, width: 500, height: 500)
            previousOrientation = UIInterfaceOrientationMask.landscapeRight
            gyro_left()
        default:
            print(" ")
        }
        
    }
    
    func gyro_up(){
        self.moto = 0.0
        self.dir = 0
        self.move = 0.0
        manager.stopGyroUpdates()
        manager.startGyroUpdates(to: OperationQueue.main){
            (data, err) in
            
            self.move = data?.rotationRate.y ?? 0
            self.moto += self.move
            if(self.move < 0.1 && self.move > -0.1){self.moto = 0}
            if self.move>0 && !self.waiting { self.dir = 1
            }else if self.move<0 && !self.waiting{ self.dir = -1 }
            if self.waiting && self.moto > -self.range && self.moto < self.range {
                self.waiting = false
            } else if !self.waiting {
                if((Int(self.move) > self.moveRangeV || Int(self.move) < -self.moveRangeV) && Int(self.move)/self.dir > 0) {
                    self.generator.impactOccurred()
                    self.moveBlock(direction: self.dir)
                    self.waiting = true
                    self.dir = 0
                }
            }
        }
    }
    func gyro_left(){
        self.moto = 0.0
        self.dir = 0
        self.move = 0.0
        manager.stopGyroUpdates()
        manager.startGyroUpdates(to: OperationQueue.main){
            (data, err) in
            
            self.move = data?.rotationRate.x ?? 0
            self.moto += self.move
            if(self.move < 0.1 && self.move > -0.1){self.moto = 0}
            if self.move>0 && !self.waiting { self.dir = 1
            }else if self.move<0 && !self.waiting{ self.dir = -1 }
            if self.waiting && self.moto > -self.range && self.moto < self.range {
                self.waiting = false
            } else if !self.waiting {
                if((Int(self.move) > self.moveRangeH || Int(self.move) < -self.moveRangeH) && Int(self.move)/self.dir > 0) {
                    self.generator.impactOccurred()
                    self.moveBlock(direction: self.dir)
                    self.waiting = true
                    self.dir = 0
                }
            }
        }
    }
    func gyro_right(){
        self.moto = 0.0
        self.dir = 0
        self.move = 0.0
        manager.stopGyroUpdates()
        manager.startGyroUpdates(to: OperationQueue.main){
            (data, err) in
            
            self.move = data?.rotationRate.x ?? 0
            self.moto += self.move
            if(self.move < 0.1 && self.move > -0.1){self.moto = 0}
            if self.move>0 && !self.waiting { self.dir = 1
            }else if self.move<0 && !self.waiting{ self.dir = -1 }
            if self.waiting && self.moto > -self.range && self.moto < self.range {
                self.waiting = false
            } else if !self.waiting {
                if((Int(self.move) > self.moveRangeH || Int(self.move) < -self.moveRangeH) && Int(self.move)/self.dir > 0) {
                    self.generator.impactOccurred()
                    self.moveBlock(direction: -self.dir)
                    self.waiting = true
                    self.dir = 0
                }
            }
        }
    }
    func gyro_down(){
        self.moto = 0.0
        self.dir = 0
        self.move = 0.0
        manager.stopGyroUpdates()
        manager.startGyroUpdates(to: OperationQueue.main){
            (data, err) in
            
            self.move = data?.rotationRate.y ?? 0
            self.moto += self.move
            if(self.move < 0.1 && self.move > -0.1){self.moto = 0}
            if self.move>0 && !self.waiting { self.dir = 1
            }else if self.move<0 && !self.waiting{ self.dir = -1 }
            if self.waiting && self.moto > -self.range && self.moto < self.range {
                self.waiting = false
            } else if !self.waiting {
                if((Int(self.move) > self.moveRangeV || Int(self.move) < -self.moveRangeV) && Int(self.move)/self.dir > 0) {
                    self.generator.impactOccurred()
                    self.moveBlock(direction: -self.dir)
                    self.waiting = true
                    self.dir = 0
                }
            }
        }
    }
    
    func moveBlock(direction:Int) {
        print("it move " + String(direction))
        if direction == -1 && player1{
            let data = client.send(string: "a")
        }else if direction == 1 && player1{
            let data = client.send(string: "d")
        }else if direction == -1 && !player1{
            let data = client.send(string: "j")
        }else if direction == 1 && !player1{
            let data = client.send(string: "l")
        }
//        self.movView.frame = CGRect(x: self.movView.frame.minX + (self.movView.frame.width * CGFloat(direction)),
//                                    y: self.movView.frame.minY,
//                                    width: self.movView.frame.width,
//                                    height: self.movView.frame.height)

    }
    
    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        return UIInterfaceOrientationMask.all
    }

//
//    override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {
//        
//        print(UIDevice.current.orientation.rawValue)
//        
////        switch UIDevice.current.orientation.rawValue {
////        case 1:
////            print("upright")
////        case 2:
////            print("upside down")
////        case 3:
////            print("rotate left")
////        case 4:
////            print("rotate right")
////        default:
////            print("_")
////        }
//    }
}

