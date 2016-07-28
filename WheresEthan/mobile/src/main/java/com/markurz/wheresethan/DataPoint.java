package com.markurz.wheresethan;

import android.os.Parcel;
import android.os.Parcelable;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by markkurtz on 4/6/16.
 */
public class DataPoint implements Parcelable {
    public static final int ROOM_AWAY = 1;
    public static final int ROOM_MAIN = 2;
    public static final int ROOM_KITCHEN = 3;
    public static final int ROOM_BEDROOM = 4;
    public static final int ROOM_BATHROOM = 5;
    
    private long mId;
    private int mRoomType;
    private long mTime;

    public DataPoint() {
        mId = -1l;
        mRoomType = 0;
        mTime = 0l;
    }

    public long getId() {
        return mId;
    }

    public void setId(long id) {
        mId = id;
    }

    public int getRoomType() {
        return mRoomType;
    }

    public void setRoomType(int roomType) {
        mRoomType = roomType;
    }

    public long getTime() {
        return mTime;
    }

    public void setTime(long time) {
        mTime = time;
    }

    public String getRoomTypeString() {
        switch (mRoomType) {
            case ROOM_AWAY:
                return "Away";
            case ROOM_MAIN:
                return "Main";
            case ROOM_KITCHEN:
                return "Kitchen";
            case ROOM_BEDROOM:
                return "Bedroom";
            case ROOM_BATHROOM:
                return "Bathroom";
            default:
                return "";
        }
    }

    public String getDateString() {
        Date date = new Date(mTime);
        DateFormat df = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");

        return df.format(date);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeLong(mId);
        dest.writeInt(mRoomType);
        dest.writeLong(mTime);
    }

    protected DataPoint(Parcel in) {
        mId = in.readLong();
        mRoomType = in.readInt();
        mTime = in.readLong();
    }

    public static final Parcelable.Creator<DataPoint> CREATOR = new Parcelable.Creator<DataPoint>() {
        @Override
        public DataPoint createFromParcel(Parcel source) {
            return new DataPoint(source);
        }

        @Override
        public DataPoint[] newArray(int size) {
            return new DataPoint[size];
        }
    };
}
