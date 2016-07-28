package com.markurz.wheresethan;

import android.app.Application;

import com.activeandroid.ActiveAndroid;

/**
 * Created by markkurtz on 4/6/16.
 */
public class WheresEthanApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        ActiveAndroid.initialize(this);
    }
}
