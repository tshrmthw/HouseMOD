package com.markurz.wheresethan;

import android.util.Log;

import com.activeandroid.ActiveAndroid;
import com.activeandroid.Model;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.activeandroid.query.Delete;
import com.activeandroid.query.Select;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by markkurtz on 4/6/16.
 */
@Table(name="DataPoints")
public class DataPointModel extends Model {
    @Column(name="Room")
    public int mRoom;
    @Column(name="Time")
    public long mTime;

    public static DataPoint save(DataPoint dataPoint) {
        if (dataPoint == null) {
            Log.d("ModelError", "Cannot save null data point");

            return null;
        }

        DataPointModel model = dataPoint.getId() == -1l ? createModel(dataPoint) : getModel(dataPoint);
        saveModel(model);
        DataPoint savedObject = objectFromModel(dataPoint, model);

        return savedObject;
    }

    public static List<DataPoint> save(List<DataPoint> points) {
        if (points == null) {
            Log.d("ModelError", "Cannot save null Games");

            return null;
        }

        List<DataPointModel> models = new ArrayList<>();
        List<DataPointModel> saveModels = new ArrayList<>();

        for (DataPoint point : points) {
            DataPointModel model;

            if (point.getId() == -1l) {
                model = createModel(point);
            } else {
                model = getModel(point);
            }

            saveModels.add(model);

            if (model == null) {
                models.add(getModel(point));
            } else {
                models.add(model);
            }
        }

        saveModels(saveModels);
        List<DataPoint> savedPoints = new ArrayList<>();

        for (int counter = 0; counter < models.size(); counter++) {
            DataPoint point = objectFromModel(points.get(counter), models.get(counter));
            savedPoints.add(point);
        }

        return savedPoints;
    }

    public static DataPoint get(long id) {
        DataPointModel model = new Select().from(DataPointModel.class).where("Id = ?", id).executeSingle();
        DataPoint point = objectFromModel(new DataPoint(), model);

        return point;
    }

    public static List<DataPoint> getAll() {
        List<DataPointModel> models = new Select().from(DataPointModel.class).execute();
        List<DataPoint> dataPoints = new ArrayList<>();

        for (DataPointModel model : models) {
            DataPoint point = objectFromModel(new DataPoint(), model);
            dataPoints.add(point);
        }

        return dataPoints;
    }

    public static void delete(long id) {
        new Delete().from(DataPointModel.class).where("Id = ?" , id).execute();
    }

    public static DataPointModel createModel(DataPoint object) {
        if (object == null) {
            return null;
        }

        DataPointModel model = new DataPointModel();

        return modelFromObject(model, object);
    }

    public static DataPointModel getModel(DataPoint object) {
        if (object == null) {
            return null;
        }

        DataPointModel model = new Select().from(DataPointModel.class).where("Id = ?", object.getId()).executeSingle();

        return modelFromObject(model, object);
    }

    public static void saveModel(DataPointModel model) {
        if (model == null) {
            return;
        }

        model.save();
    }

    public static void saveModels(List<DataPointModel> models) {
        if (models == null) {
            return;
        }

        ActiveAndroid.beginTransaction();
        try {
            for (DataPointModel model : models) {
                saveModel(model);
            }

            ActiveAndroid.setTransactionSuccessful();
        }
        finally {
            ActiveAndroid.endTransaction();
        }
    }

    private static DataPoint objectFromModel(DataPoint dataPoint, DataPointModel model) {
        dataPoint.setId(model.getId());
        dataPoint.setRoomType(model.mRoom);
        dataPoint.setTime(model.mTime);

        return dataPoint;
    }

    private static DataPointModel modelFromObject(DataPointModel model, DataPoint dataPoint) {
        model.mRoom = dataPoint.getRoomType();
        model.mTime = dataPoint.getTime();

        return model;
    }
}
