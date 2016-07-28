package com.markurz.wheresethan;

import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;

/**
 * Created by markkurtz on 4/6/16.
 */
public class DataPointViewHolder extends RecyclerView.ViewHolder {
    public final FrameLayout card;
    public final TextView roomText;
    public final TextView dateText;

    public DataPointViewHolder(View itemView) {
        super(itemView);

        card = (FrameLayout) itemView;
        roomText = (TextView) itemView.findViewById(R.id.room_text);
        dateText = (TextView) itemView.findViewById(R.id.date_text);
    }
}
