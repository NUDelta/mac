//
//  ViewController.swift
//  mac-ios
//
//  Created by Yongsung on 3/31/17.
//  Copyright © 2017 Delta. All rights reserved.
//

import UIKit
import MapKit
import CoreLocation

class ViewController: UIViewController, MKMapViewDelegate, CLLocationManagerDelegate {

    @IBOutlet weak var mapView: MKMapView!

    let regionRadius: CLLocationDistance = 500
    var locationManager:CLLocationManager?

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        locationManager = CLLocationManager()

        let initialLocation = CLLocation(latitude: 42.060126, longitude: -87.674241)
        let coordinateRegion = MKCoordinateRegionMakeWithDistance(initialLocation.coordinate,
                                                                  regionRadius * 2.0, regionRadius * 2.0)
        mapView.delegate = self
        mapView.setRegion(coordinateRegion, animated: false)
        mapView.showsUserLocation = true
        locationManager?.delegate = self
        locationManager?.desiredAccuracy = kCLLocationAccuracyBest
        locationManager?.activityType = .fitness
        locationManager?.distanceFilter = CLLocationDistance(10)
        if CLLocationManager.authorizationStatus() == .notDetermined {
            locationManager?.requestAlwaysAuthorization()
            locationManager?.requestWhenInUseAuthorization()
        }
        
        // We should always enable this for background location tracking.
//        locationManager!.allowsBackgroundLocationUpdates = true
//        locationManager!.pausesLocationUpdatesAutomatically = true
    }
    
    func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
        //mapView.centerCoordinate = userLocation.location!.coordinate
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

