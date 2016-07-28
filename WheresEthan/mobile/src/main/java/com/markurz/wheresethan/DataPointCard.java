package com.markurz.wheresethan;

import android.view.View;

/**
 * Created by markkurtz on 4/6/16.
 */
public class DataPointCard {
    private DataPoint mPoint;
    private InteractionListener mListener;

    public DataPointCard(DataPoint point) {
        mPoint = point;
    }

    public DataPointCard(DataPoint point, InteractionListener listener) {
        mPoint = point;
        mListener = listener;
    }

    public void bindViewHolder(final DataPointViewHolder viewHolder) {
        viewHolder.card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mListener != null) {
                    mListener.cardClicked(mPoint);
                }
            }
        });
        viewHolder.roomText.setText(mPoint.getRoomTypeString());
        viewHolder.dateText.setText(mPoint.getDateString());
    }

    public interface InteractionListener {
        void cardClicked(DataPoint point);
    }
}
