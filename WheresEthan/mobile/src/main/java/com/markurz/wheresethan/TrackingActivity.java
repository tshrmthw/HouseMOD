package com.markurz.wheresethan;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Debug;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class TrackingActivity extends AppCompatActivity {
    private List<DataPoint> mPoints;

    private DataPointsRecyclerAdapter mAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tracking);
        mPoints = DataPointModel.getAll();

        if (mPoints == null) {
            mPoints = new ArrayList<>();
            DataPoint firstPoint = new DataPoint();
            firstPoint.setTime(Calendar.getInstance().getTime().getTime());
            firstPoint.setRoomType(DataPoint.ROOM_AWAY);
            mPoints.add(firstPoint);
        }

        setupRadios();
        setupExportButton();
        setupPointCards();
        refreshPointCards();
    }

    private void setupRadios() {
        RadioGroup group = (RadioGroup) findViewById(R.id.radios_holder);

        if (group == null) {
            return;
        }

        int lastType = mPoints.isEmpty() ? DataPoint.ROOM_AWAY : mPoints.get(mPoints.size() - 1).getRoomType();

        switch (lastType) {
            case DataPoint.ROOM_AWAY:
                group.check(R.id.away_radio);

                break;
            case DataPoint.ROOM_MAIN:
                group.check(R.id.main_radio);

                break;
            case DataPoint.ROOM_KITCHEN:
                group.check(R.id.kitchen_radio);

                break;
            case DataPoint.ROOM_BEDROOM:
                group.check(R.id.bedroom_radio);

                break;
            case DataPoint.ROOM_BATHROOM:
                group.check(R.id.bathroom_radio);

                break;
            default:
                group.check(R.id.away_radio);

                break;
        }

        RadioButton awayRadio = (RadioButton) findViewById(R.id.away_radio);
        if (awayRadio != null) {
            awayRadio.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    DataPoint point = new DataPoint();
                    point.setTime(Calendar.getInstance().getTime().getTime());
                    point.setRoomType(DataPoint.ROOM_AWAY);
                    point = DataPointModel.save(point);
                    mPoints.add(point);
                    refreshPointCards();
                }
            });
        }

        RadioButton mainRadio = (RadioButton) findViewById(R.id.main_radio);
        if (mainRadio != null) {
            mainRadio.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    DataPoint point = new DataPoint();
                    point.setTime(Calendar.getInstance().getTime().getTime());
                    point.setRoomType(DataPoint.ROOM_MAIN);
                    point = DataPointModel.save(point);
                    mPoints.add(point);
                    refreshPointCards();
                }
            });
        }

        RadioButton kitchenRadio = (RadioButton) findViewById(R.id.kitchen_radio);
        if (kitchenRadio != null) {
            kitchenRadio.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    DataPoint point = new DataPoint();
                    point.setTime(Calendar.getInstance().getTime().getTime());
                    point.setRoomType(DataPoint.ROOM_KITCHEN);
                    point = DataPointModel.save(point);
                    mPoints.add(point);
                    refreshPointCards();
                }
            });
        }

        RadioButton bedroomRadio = (RadioButton) findViewById(R.id.bedroom_radio);
        if (bedroomRadio != null) {
            bedroomRadio.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    DataPoint point = new DataPoint();
                    point.setTime(Calendar.getInstance().getTime().getTime());
                    point.setRoomType(DataPoint.ROOM_BEDROOM);
                    point = DataPointModel.save(point);
                    mPoints.add(point);
                    refreshPointCards();
                }
            });
        }

        RadioButton bathroomRadio = (RadioButton) findViewById(R.id.bathroom_radio);
        if (bathroomRadio != null) {
            bathroomRadio.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    DataPoint point = new DataPoint();
                    point.setTime(Calendar.getInstance().getTime().getTime());
                    point.setRoomType(DataPoint.ROOM_BATHROOM);
                    point = DataPointModel.save(point);
                    mPoints.add(point);
                    refreshPointCards();
                }
            });
        }
    }

    private void setupExportButton() {
        View exportButton = findViewById(R.id.export_button);

        if (exportButton == null) {
            return;
        }

        exportButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                verifyStoragePermissions(TrackingActivity.this);

                File file = new File(Environment.getExternalStorageDirectory(), "wheresEthanDataPoints.txt");

                try {
                    if (file.exists()) {
                        file.delete();
                    }

                    file.createNewFile();
                    FileOutputStream stream = new FileOutputStream(file);
                    OutputStreamWriter writer = new OutputStreamWriter(stream);
                    String separator = System.getProperty("line.separator");

                    for (DataPoint point : mPoints) {
                        String line = "{\"type\":" + Integer.toString(point.getRoomType()) + ",\"typeString\":\"" + point.getRoomTypeString() + "\",\"time\":" + Long.toString(point.getTime()) + "}";
                        writer.append(line);
                        writer.append(separator);
                    }

                    writer.flush();
                    writer.close();
                    stream.close();
                } catch (Exception ex) {
                    Log.d("WheresEthan", ex.toString());
                }
            }
        });
    }

    private void setupPointCards() {
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.points_recycler_view);

        if (recyclerView == null) {
            return;
        }

        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        mAdapter = new DataPointsRecyclerAdapter();
        recyclerView.setAdapter(mAdapter);
    }

    private void refreshPointCards() {
        mAdapter.getDataPointCards().clear();

        for (int counter = mPoints.size() - 1; counter >= 0; counter--) {
            final int pointPosition = counter;
            mAdapter.getDataPointCards().add(new DataPointCard(mPoints.get(counter), new DataPointCard.InteractionListener() {
                @Override
                public void cardClicked(DataPoint point) {
                    DataPointModel.delete(point.getId());
                    mPoints.remove(pointPosition);
                    refreshPointCards();
                }
            }));
        }

        mAdapter.notifyDataSetChanged();
    }

    private static final int REQUEST_EXTERNAL_STORAGE = 1;
    private static String[] PERMISSIONS_STORAGE = {
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    };

    public static void verifyStoragePermissions(Activity activity) {
        // Check if we have write permission
        int permission = ActivityCompat.checkSelfPermission(activity, Manifest.permission.WRITE_EXTERNAL_STORAGE);

        if (permission != PackageManager.PERMISSION_GRANTED) {
            // We don't have permission so prompt the user
            ActivityCompat.requestPermissions(
                    activity,
                    PERMISSIONS_STORAGE,
                    REQUEST_EXTERNAL_STORAGE
            );
        }
    }
}
